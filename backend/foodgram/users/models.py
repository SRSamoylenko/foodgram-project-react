from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('Email address'),
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=150,
    )
    follows = models.ManyToManyField(
        to='self',
        through='Follow',
        related_name='followers',
        symmetrical=False,
        verbose_name=_('Following'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta(AbstractUser.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='+',
        verbose_name=_('Follower'),
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        User,
        related_name='+',
        verbose_name=_('Following'),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        constraints = (
            models.UniqueConstraint(
                name='unique_followers',
                fields=('from_user', 'to_user'),
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(from_user=models.F('to_user')),
            ),
        )
        ordering = ('id',)

    def __str__(self):
        return (
            _('{} follows {}').format(self.from_user, self.to_user)
        )

    def clean(self):
        if self.from_user == self.to_user:
            raise ValidationError('User can not follow himself.')
        return super(Follow, self).clean()
