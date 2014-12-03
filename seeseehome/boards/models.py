from django.db import models
from users.models import User
#from posts.models import Post
from seeseehome import msg
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from multiselectfield import MultiSelectField

class BoardManager(models.Manager):
##### CREATE
    def _create_board(self, boardname):
        self.validate_boardname(boardname)
        self.validate_max_number_of_boards(Board.objects.all().count())
        board = self.model(boardname = boardname)
        board.save(using=self._db)
        return board

    def create_board(self, boardname):
        return self._create_board(boardname)

    def validate_max_number_of_boards(self, num_of_boards):
#       Number of Boards are already more than or equal to 10?        
        if num_of_boards >= 10:
            raise ValidationError(msg.boards_max_number_of_boards)
        return True

    def validate_boardname(self, boardname):
        if not boardname:
            raise ValueError(msg.boards_name_must_be_set)
        elif len(boardname) > 30:
            raise ValidationError(msg.boards_name_at_most_30)
        return True

    def is_valid_readperm(self, board, reader):
        return bool(str(board.readperm).find(reader.userperm) >= 1)


##########
##### RETRIEVE
    def get_board(self, id):
        try:
            return Board.objects.get(pk=id)
        except Board.DoesNotExist:
            return None

##########
##### UPDATE : This is only applied in admin page.
    def update_board(self, id, **extra_fields):
        board = Board.objects.get_board(id)
        if 'boardname' in extra_fields:
            self.validate_boardname(extra_fields['boardname'])
            board.boardname = extra_fields['boardname']
        else:
            raise ValueError()
        board.save(using = self._db)

##########
##### DELETE
    def delete_board(self, id):
        board = Board.objects.get(id=id)
        board.delete()

class Board(models.Model):
    objects = BoardManager()

    boardname = models.CharField(
                    help_text = "Board name",
                    max_length = 255,
                    default = '',
                )

    """
    * Warning : char field is set to unicode
    """
    readperm = MultiSelectField(
                    help_text = ('Available Read Permission (It is possible'
                    ' to select multiple[ User, Member, '
                    'Core member, Graduate, President ]'),
                    choices = (('1', 'User'), ('2', 'Member'), 
                        ('3', 'Core member'), ('4', 'Graduate'), 
                        ('5', 'President')),
                    default = ['1','2','3','4','5'],
                    max_length = 9,
                    max_choices=5,
               )
                   
    writeperm = MultiSelectField(
                    help_text = ('Available Write Permission (It is possible'
                    'to select multiple[ User, Member, '
                    'Core member, Graduate, President ]'),
                    choices = (('1', 'User'), ('2', 'Member'), 
                        ('3', 'Core member'), ('4', 'Graduate'), 
                        ('5', 'President')),
                    default = ['1', '2', '3', '4', '5'],
                    max_length = 9,
                    max_choices=5,
               )

#   for showing user name instead of object itself in admin page
    def __unicode__(self):
       return 'Board name: ' + self.boardname
 

class PostManager(models.Manager):
    ##### CREATE
    def _create_post(self, board, subject, writer, **extra_fields):
        is_valid_content = False
        is_valid_writer = False

#       subject
        self.validate_subject(subject)

#       content
        if 'content' in extra_fields:
            content = extra_fields['content']
            is_valid_content = self.validate_content(content)

#       writer
        is_valid_writer = self.is_valid_writeperm(
                              board = board, 
                              writer = writer
                          )
        if not is_valid_writer:
            raise ValidationError(msg.boards_writer_perm_error)

#       post save ( caution : board is not parameter for post model )
        post = self.model(subject=subject, writer=writer)
        
        if is_valid_content:
            post.content = content

        post.save(using=self._db)
             
        # create a relationship between board & post
        boardposts = BoardPosts.objects.create_board_posts(
                             board = board,
                             post = post,
                         )
        boardposts.save()
        return post

    def create_post(self, board, subject, writer, **extra_fields):
        return self._create_post(board=board, subject=subject, writer=writer,
                **extra_fields)
    
    def validate_subject(self, subject):
        if not subject:
            raise ValueError(msg.boards_post_subject_must_be_set)
        elif len(subject) > 255:
            raise ValidationError(msg.boards_post_subject_at_most_255)
    
    def validate_content(self, content):
       if len(content) > 65535:
            raise ValidationError(msg.boards_post_content_at_most_255)
       else:
            return True

    def is_valid_writeperm(self, board, writer):
        return bool(str(board.writeperm).find(writer.userperm) >= 1)

        """
        Following code is more simple and operates well,
        but it occurs some problems in the test codes
        ( double wrapping of unicode & list )
        """
#        return bool(writer.userperm in board.writeperm)

    ##########
    ##### RETRIEVE
    def get_post(self, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    ##########
    ##### UPDATE
    def update_post(self, post_id, **extra_fields):
        post = Post.objects.get_post(post_id)
        if 'subject' in extra_fields:
            post.subject = extra_fields['subject']
        if 'content' in extra_fields:
            post.content = extra_fields['content']

        post.save()

class Post(models.Model):
    objects = PostManager()
    writer = models.ForeignKey(User)
    subject = models.CharField(
                  help_text = "Post subject",
                  max_length = 255,
                  default = '',
              )

    content = models.TextField(
                  help_text = "Post content",
                  max_length = 65535,
                  default = '',
              )
    
    posts = models.ManyToManyField(
                Board,
                verbose_name = "board posts of many to many field",
                through = 'BoardPosts',
                through_fields = ('post', 'board'),
                related_name="posts_mtom"
            )

#   It is used to show date posted in admin page 
    date_posted = models.DateTimeField(db_index=True, auto_now_add=True, 
            help_text = "It is used to show date posted in admin page")
    
#   for showing user name instead of object itself
    def __unicode__(self):
       return ('Writer: ' + self.writer.username + ", " +\
                "Subject: " + self.subject)

class BoardPostsManager(models.Manager):
    def _create_board_posts(self, board, post):
        # The precise validator for This method is not implemented.
        # This method should be called in create_post method.
        if board.__class__.__name__ is not "Board":
            raise ValidationError(msg.boards_board_arg_error)
        if post.__class__.__name__ is not "Post":
            raise ValidationError(msg.boards_post_arg_err)

        board_posts = self.model(board=board, post=post)
        board_posts.save(using=self._db)
        return board_posts

    def create_board_posts(self, board, post):
        return self._create_board_posts(board, post)

class BoardPosts(models.Model):
    objects = BoardPostsManager()
    
    board = models.ForeignKey(
                Board,
                verbose_name = "board foreign key",
                related_name="board_foreignkey",
            )

    post = models.ForeignKey(
               Post,
               verbose_name = "post foreign key",
               related_name="post_foreignkey",
            )

#  It is used to show data in orders in board page    
    date_board_posts_created = \
            models.DateTimeField(
                db_index=True, auto_now_add=True,
                help_text = "It is used to show data in orders in board page"
            )
 
