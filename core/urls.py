from django.conf.urls import patterns, url

from .views import QuestionView, QuestionListView, PopularQuestionListView, \
    MyUserListView, AskQuestionView, MyUserView, MyUserQuestionListView, TagListView, BookmarksView, Members

from django.contrib.auth import get_user_model as user_model
MyUser = user_model()

urlpatterns = patterns('',
    url(r'^$', QuestionListView.as_view(), name='home'),
    url(r'^question/ask/$', AskQuestionView.as_view(), name='ask_question'),
    url(r'^question/(?P<questionid>.+)/$', QuestionView.as_view(), name='question'),

    url(r'^questions/latest/$', QuestionListView.as_view(), name='questions_latest'),
    url(r'^questions/popular/$', PopularQuestionListView.as_view(), name='questions_popular'),
    url(r'^questions/$', QuestionListView.as_view(), name='questions'),
    url(r'^user/(?P<username>.+)/questions/$', MyUserQuestionListView.as_view(), name='user_questions'),

    url(r'^user/(?P<username>.+)/$', MyUserView.as_view(), name='user'),
    url(r'^users/$', MyUserListView.as_view(), name='users'),

    url(r'^home/$', AskQuestionView.as_view(), name='home'),
    url(r'^search2/$', QuestionListView.as_view(), name='search_results'),

    url(r'^tags/$', TagListView.as_view(template_name='core/tag_list.html'), name='tags'),
    url(r'^tag/(?P<tag>.+)/$', QuestionListView.as_view(template_name='core/question_list.html'), name='tag'),

    url(r'^bookmarks2/', BookmarksView.as_view(template_name='core/bookmark_list.html'), name='bookmarks_list'),

    # temp, should be deleted
    url(r'^members/$', Members.as_view(), name='members'),
    )
