class FatalServiceError(RuntimeError):
    """
    Error grave que debe terminar el proceso
    para que systemd lo vuelva a iniciar.
    """