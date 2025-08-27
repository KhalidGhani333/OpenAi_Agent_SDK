from agents import (
    RunContextWrapper
)


async def tool_validate(ctx:RunContextWrapper,agent):
    if ctx.context["isPremium"] == "True":
        return True
    return False