from abc import ABC, abstractmethod

from langchain.chat_models import ChatOpenAI

from chatgpt_wrapper.core.config import Config
from chatgpt_wrapper.core.logger import Logger

class PluginBase(ABC):
    def __init__(self, config=None):
        self.config = config or Config()
        self.log = Logger(self.__class__.__name__, self.config)

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def default_config(self):
        pass

    def set_name(self, name):
        self.name = name

    def set_backend(self, backend):
        self.backend = backend

    def set_shell(self, shell):
        self.shell = shell

    def get_shell_completions(self, _base_shell_completions):
        pass

    def get_default_llm_args(self):
        return {
            'temperature': 0,
            'model_name': self.backend.model,
            # TODO: This used to work on the deprecated OpenAIChat class, but now no longer works.
            # 'prefix_messages': [
            #     {
            #         'role': 'system',
            #         'content': 'You are a helpful assistant that is very good at problem solving who thinks step by step.',
            #     },
            # ]
        }

    def make_llm(self, args={}):
        final_args = self.get_default_llm_args()
        final_args.update(args)
        llm = ChatOpenAI(**final_args)
        return llm

    def query_llm(self, messages):
        llm = self.make_llm()
        try:
            result = llm(messages)
            result_string = result.content
        except ValueError as e:
            return False, None, e
        return True, result, result_string

class Plugin(PluginBase):

    @abstractmethod
    def setup(self):
        pass
