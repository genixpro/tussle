from tussle.integrations.openai.openai_integration import OpenAIIntegration
from tussle.general.logger import get_logger
from dependency_injector.wiring import inject, Provide
from .health_check_base import HealthCheckBase
import traceback



class OpenAIIntegrationHealthCheck(HealthCheckBase):
    """This verifies that the integration with openai is working and returning completion results."""

    @inject
    def __init__(self,
                    openai_integration: OpenAIIntegration = Provide['openai_integration'],
                 ):
        super().__init__()
        self.openai_integration = openai_integration
        self.logger = get_logger("OpenAIIntegrationHealthCheck")

    def check(self):
        try:
            test_prompt = "this is a testing prompt, used in unit tests and integrations. please just print 'yes sir. acknowledged' and nothing else."

            result = self.openai_integration.completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": test_prompt}],
                temperature=0,
                stream=False,
            )

            message_content = result.choices[0].message.content.strip().lower()

            healthy = message_content == "yes sir. acknowledged"

            self.logger.debug(f"OpenAI integration test result: Healthy: {healthy}. Details: message_content: \"{message_content}\"")
            return {
                "healthy": healthy,
                "details": {
                    "message_content": message_content
                }
            }
        except Exception as e:
            self.logger.error(f"Error while checking openai integration check:\n{traceback.format_exc()}")
            return {
                "healthy": False,
                "details": {
                    "error": traceback.format_exc()
                }
            }
