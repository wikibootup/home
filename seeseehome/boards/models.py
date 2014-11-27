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

class PostManager(models.Manager):
    ##### CREATE
    def _create_post(self, board, writer, subject, content):
        Board.objects.validate_boardname(board.boardname)
        User.objects.validate_username(writer.username)
        self.validate_subject(subject)
        self.validate_content(content)
        post = self.model(writer=writer, subject=subject,
                content=content)        
        post.save(using=self._db)
             
        # create a relationship between board & post
        board_posts = BoardPosts.objects.create_board_posts(
                             board = board,
                             post = post,
                         )
        board_posts.save()
        return post

    def create_post(self, board, writer, subject, content):
        return self._create_post(board, writer, subject, content)
    
    def validate_subject(self, subject):
        if not subject:
            raise ValueError(msg.boards_post_subject_must_be_set)
        elif len(subject) > 255:
            raise ValidationError(msg.boards_post_subject_at_most_255)
    
    def validate_content(self, content):
        if not content:
            raise ValueError(msg.boards_post_content_must_be_set)
        elif len(content) > 65535:
            raise ValidationError(msg.boards_post_content_at_most_255)

    ##########
    ##### RETRIEVE
    def get_post(self, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

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
    posted_date = models.DateField(db_index=True, auto_now_add=True)
    
    
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

