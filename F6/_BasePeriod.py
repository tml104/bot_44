import abc


class _BasePeriod(abc.ABC):
    repeat_time: int

    @classmethod
    @abc.abstractmethod
    async def create(cls) -> "_BasePeriod":
        raise NotImplementedError()

    @abc.abstractmethod
    async def enter_loop(self, *, bot):
        raise NotImplementedError()
