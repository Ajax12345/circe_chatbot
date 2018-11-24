import re, collections, typing
import datetime

class chatRedirect:
    def __init__(self, _to_node:int) -> None:
        self.to_node = _to_node


class Chatterbot:
    digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    class _chatResponse(typing.NamedTuple):
        html:str
        next_node:typing.Any


    class ChatterbotResponse:
        def __init__(self, _message:str, _next_node:int, subsequent:typing.List[typing.Callable] = []) -> None:
            self.message = _message
            self._next = _next_node
            self.subsequent = subsequent
            self.time_sent = datetime.datetime.now()
        def __repr__(self):
            return f'<Response message="{self.message[:20]}...." next="{self._next}", subsequent_num="{len(self.subsequent)}">'
    class _finis:
        def __init__(self) -> None:
            self._id = 'end'
        def __eq__(self, _val:str) -> bool:
            return _val == self._id
        def __repr__(self):
            return '<chat "end">'
        
    def __init__(self, _name:str) -> None:
        self._app_name = _name
        self._register = collections.defaultdict(list)
        self.end_chat = self.__class__._finis()

    def build(self, _message:str, _seq:int) -> str:
        _main, *_trailing = self._register[_seq]
        _full_response = _main() if not _seq else _main(_message)
        if isinstance(_full_response, chatRedirect):
            return self.build(_message, _full_response.to_node)
        _html = f'''
        <div style='height:{"50px" if not _seq else "120px"}'></div>
        <div class='circe_response'>
            <p class='circe_text'>{_full_response.message}</p>
        </div>
        '''
        _subsequent_html = """
        <div style='height:10px;'></div>
        <div class='circe_subsequent_response'>
             <p class='circe_text'>{}</p>
        </div>
        """
        return self.__class__._chatResponse(_html+'\n'+'\n'.join(_subsequent_html.format(i()) for i in _full_response.subsequent), 'end' if _full_response._next == 'end' else _full_response._next)
    def welcome(self, _f:typing.Callable) -> typing.Callable[[typing.Any], int]:
       
        self._register[0].extend([_f])
        return _f

    def chatterstream(self, _node:int) -> typing.Callable:
        def _wrapper(_f:typing.Callable) -> typing.Callable[[typing.Any], int]:
            self._register[_node].extend([_f])

        return _wrapper


if __name__ == '__main__':  
    chatter = Chatterbot('circe')

    @chatter.welcome
    def first_message():
        return Chatterbot.ChatterbotResponse("Hello! I am Circe, and I would like to converse with you about the Humanities", 1)


    @chatter.chatterstream(1)
    def second_result(_val):
        return Chatterbot.ChatterbotResponse("we are testing our data for now", 2)

    @chatter.chatterstream(2)
    def third_val(_val):
        return chatRedirect(4)

    @chatter.chatterstream(4)
    def fourth_val(val):
        return Chatterbot.ChatterbotResponse('Yes!!!!', chatter.end_chat)


 

