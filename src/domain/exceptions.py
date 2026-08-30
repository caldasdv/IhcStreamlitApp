"""Exceções de domínio compartilhadas pelas camadas da aplicação."""


class EntityNotFoundError(LookupError):
    """Indica que uma escrita não encontrou a entidade no escopo do usuário."""


class DuplicateSubjectError(ValueError):
    """Indica que o usuário já possui uma disciplina com o mesmo nome."""


class DuplicateAcademicPeriodError(ValueError):
    """Indica que o usuário já possui um período acadêmico com o mesmo nome."""
