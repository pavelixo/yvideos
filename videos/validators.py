import os
from secrets import token_urlsafe

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from magic import from_buffer


@deconstructible
class VideoValidator:
    allowed_ext = [".mp4", ".avi", ".mov", ".mkv"]
    allowed_mime = [
        "video/mp4",
        "video/avi",
        "video/quicktime",
        "video/x-matroska",
    ]
    message_ext = _("Extensão inválida — os arquivos permitidos são: %(ext)s")
    message_mime = _("Tipo MIME inválido — não parece um vídeo compatível: %(mime)s")
    code = "invalid_video"

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in self.allowed_ext:
            raise ValidationError(
                self.message_ext % {"ext": ", ".join(self.allowed_ext)}, code=self.code
            )
        value.open()
        mime = from_buffer(value.read(2048), mime=True)
        value.seek(0)
        if mime not in self.allowed_mime:
            raise ValidationError(self.message_mime % {"mime": mime}, code=self.code)

    def __eq__(self, other):
        return isinstance(other, VideoValidator)


@deconstructible
class NameValidator:
    message = _("Não foi possível gerar nome válido para o arquivo.")

    code = "invalid_name"
    token_bytes = 16  # gera string de ~43 caracteres em base64-url

    def __call__(self, value):
        _, ext = os.path.splitext(value.name)
        if not ext:
            raise ValidationError(self.message, code=self.code)

        token = token_urlsafe(self.token_bytes)
        value.name = f"{token}{ext.lower()}"

    def __eq__(self, other):
        return isinstance(other, NameValidator)
