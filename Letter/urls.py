from django.urls import path
from Letter.views import LetterDataView, AttachmentTypeView, FileUpload


urlpatterns = [
    path('letter_data/', LetterDataView.as_view()),
    path('attachment_type/', AttachmentTypeView.as_view()),
    path('file/', FileUpload.as_view()),
]
