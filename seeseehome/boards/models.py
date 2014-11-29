from django.db import models
from users.models import User
#from posts.models import Post
from seeseehome import msg
from django.core.exceptions import ObjectDoesNotExist,ValidationError

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
        if num_of_boards > 10:
            raise ValidationError(msg.boards_max_number_of_boards)
        return True

    def validate_boardname(self, boardname):
        if not boardname:
            raise ValueError(msg.boards_name_must_be_set)
        elif len(boardname) > 30:
            raise ValidationError(msg.boards_name_at_most_30)
        return True

##########
##### RETRIEVE
    def get_board(self, id):
        try:
            return Board.objects.get(pk=id)
        except Board.DoesNotExist:
            return None

##########
##### UPDATE
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
                    help_text = "Board subject",
                    max_length = 255,
                    default = '',
                )

    readperm = models.IntegerField(
                   help_text = "Read permission ( anonymous :0, user : 1, "
                   "member : 2, coremember : 4, graduate : 8, "
                   "president : 16, all : 31 )",
                   default=msg.perm_all
               )
    writeperm = models.IntegerField(
                    help_text = "Read permission ( anonymous :0, user : 1, "
                    "member : 2, coremember : 4, graduate : 8, "
                    "president : 16, all : 31 )",
                    default=msg.perm_all
                )

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
        is_valid_writer = self.is_valid_perm(
                              boardperm = board.writeperm, 
                              userperm = writer.userperm
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

    def is_valid_perm(self, boardperm, userperm):
        return bool(boardperm & userperm)

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

    posted_date = models.DateTimeField(db_index=True, auto_now_add=True)
    
