
class Star:
    """
    Represents a Starred message
    """

    def __init__(self, message_id: int, author: str, title: str, content: str, img_url: str):
        self.message_id = message_id
        self.author = author
        self.title = title
        self.content = content
        self.img_url = img_url


class StarQueue:
    """
    A FIFO queue of stars
    """
    
    def __init__(self):
        self.queue = []
        
    @property
    def queue(self):
        return self.queue

    def append(self, star):
        self.queue.append(star)

    def pop(self):
        return self.queue.pop(0)
