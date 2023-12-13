from tussle.general.logger import get_logger
import openai
import tenacity
import traceback
from pprint import pformat


class OpenAIIntegration:
    logger = get_logger("openai")
    completion_timeout = 60
    embedding_timeout = 10
    # Limit the number of completions that are allowed to come from the same machine
    completion_rate_limit_tokens_per_minute = 15000
    # Embeddings have a much higher rate limit
    embedding_rate_limit_tokens_per_minute = 50000
    rate_limit_window_time = 10
    track_completion_times = False
    track_embedding_times = False

    def __init__(self, config):
        self.enabled = False

        self.client = openai.OpenAI(
            api_key=config['openai']['key'],
            base_url=config['openai'].get('api_base'),
            # We disable retries as we handle retries inside our own code.
            max_retries=0,
        )

        openai.api_key = config['openai']['key']
        if config['openai']['enabled']:
            self.enabled = True
            self.logger.info(f"Connecting to OpenAI using the host {self.client.base_url}")


    def check_openai_connection(self):
        """
        This function is used to verify that the server has a working OpenAI API key and is able
        to connect and execute API calls with OpenAI.
        :return:
        """
        models = self.client.models.list()
        assert len(models) > 1
        self.logger.info(f"Successfully connected to OpenAI API. Received a list of {len(models)} models.")

    def completion(self, *args, **kwargs):
        """
        This function gets a completion from openai, without any retries.
        :return:
        """
        if not self.enabled:
            # raise RuntimeError("A completion was requested even though OpenAI is disabled.")
            self.logger.warning("A completion was requested even though OpenAI is disabled.")

        try:
            result = self.client.chat.completions.create(*args, **kwargs)
            return result
        except openai.Timeout as e:
            # Pass through without logging it. This is a common error seen when using OpenAI APIs.
            raise e
        except Exception as e:
            self.logger.warning(f"Warning, an error fetching completion for input {pformat(args)}, {pformat(kwargs)}:\n{traceback.format_exception(e)}. Will retry if attempts not exhausted.")
            raise e

    @tenacity.retry(
        wait=tenacity.wait_exponential_jitter(initial=2, exp_base=2),
        retry_error_callback=lambda state: OpenAIIntegration.logger.warning(f"Warning, error received while fetching completion for prompt {pformat(state.args)}, {pformat(state.kwargs)}:\n{traceback.format_exception(state.outcome.exception())}. Will retry if attempts not exhausted."),
        stop=tenacity.stop_after_attempt(8),
        retry=tenacity.retry_if_exception_type((
            openai.APIConnectionError,
            openai.InternalServerError,
            openai.RateLimitError,
            openai.APITimeoutError
        ))
    )
    def completion_with_retry(self, *args, **kwargs):
        """
        This function handles retries for the openai.Completion.create() function, allowing us
        to smoothly handle situations where there is connection errors or rate limiting errors
        :param kwargs:
        :return:
        """
        kwargs['timeout'] = self.completion_timeout

        return self.completion(*args, **kwargs)


    def embedding(self, *args, **kwargs):
        """
        This function handles fetches an embedding, without any retries
        :param kwargs:
        :return:
        """
        if not self.enabled:
            # raise RuntimeError("An embedding was requested even though OpenAI is disabled.")
            self.logger.warning("An embedding was requested even though OpenAI is disabled.")
        try:
            embedding = self.client.embeddings.create(*args, **kwargs)
            return embedding
        except openai.Timeout as e:
            # Pass through without logging it. This is a common error seen when using OpenAI APIs.
            raise e
        except Exception as e:
            self.logger.error(f"Warning. Error received while fetching embedding for text {pformat(args)}, {pformat(kwargs)}:\n{traceback.format_exception(e)}. Will retry if attempts not exhausted.")
            raise e


    @tenacity.retry(
        wait=tenacity.wait_exponential_jitter(initial=2, exp_base=2),
        stop=tenacity.stop_after_attempt(8),
        retry_error_callback=lambda state: OpenAIIntegration.logger.warning(f"Warning, error received while fetching embedding for text {pformat(state.args)}, {pformat(state.kwargs)}:\n{traceback.format_exception(state.outcome.exception())}. Will retry if attempts not exhausted."),
        retry=tenacity.retry_if_exception_type((
            openai.APIConnectionError,
            openai.InternalServerError,
            openai.RateLimitError,
            openai.APITimeoutError
        ))
    )
    def embedding_with_retry(self, *args, **kwargs):
        """
        This function handles retries for the openai.Embedding.create() function, allowing us
        to smoothly handle situations where there is connection errors or rate limiting errors
        :param kwargs:
        :return:
        """
        kwargs['timeout'] = self.completion_timeout

        return self.embedding(*args, **kwargs)

    def upload_file(self, file_stream):
        return self.client.files.create(
            file=file_stream,
            purpose="fine-tune"
        )

    def delete_file(self, file_id):
        return self.client.files.delete(
            file_id=file_id
        )

    def start_fine_tuning_job(self, training_file_id, model="gpt-3.5-turbo"):
        return self.client.fine_tuning.jobs.create(
          training_file=training_file_id,
          model=model
        )


