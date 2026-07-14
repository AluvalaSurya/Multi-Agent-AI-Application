#as of now aggregator is not needed but if it scales now its 3 agents
#if suppose there are multiple agents then ResponseAgent shouldn't receive everything.
# Aggregator can summarize first.

class Aggregator:

    async def run(self, state):

        # Future enhancements:
        # - Merge metadata
        # - Filter failed agents
        # - Track execution statistics

        return state