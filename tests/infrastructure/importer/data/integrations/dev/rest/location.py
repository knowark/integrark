
class Location:
    path = 'media'

    async def route(self, context):
        return (
            f"HTTP Response from '{self.path}' with context {str(context)}")
