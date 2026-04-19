import traceback


class DetailedException(Exception):
    """Exception that exposes the originating file, line, and original error details."""

    def __init__(self, message: str, file_name: str | None = None, line_number: int | None = None, original_exception: Exception | None = None):
        self.file_name = file_name
        self.line_number = line_number
        self.original_exception = original_exception

        details = []
        if file_name is not None:
            details.append(f"File '{file_name}'")
        if line_number is not None:
            details.append(f"line {line_number}")
        if original_exception is not None:
            details.append(f"original error: {original_exception!r}")

        detail_text = ", ".join(details) if details else ""
        if detail_text:
            super().__init__(f"{message} ({detail_text})")
        else:
            super().__init__(message)

    @classmethod
    def from_exception(cls, exc: BaseException, message: str | None = None):
        tb = exc.__traceback__
        if tb is None:
            return cls(message or str(exc), original_exception=exc)

        last_frame = traceback.extract_tb(tb)[-1]
        file_name = last_frame.filename
        line_number = last_frame.lineno
        exc_message = message or str(exc)
        return cls(exc_message, file_name=file_name, line_number=line_number, original_exception=exc)

    def __str__(self) -> str:
        base = super().__str__()
        if self.original_exception is not None and self.original_exception is not self:
            return f"{base}: {self.original_exception}"
        return base
