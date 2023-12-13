import {getPromptElement} from "../support/e2e";
import { testChartAppUrl } from "../support/config";
import "../support/disable_motion";

describe('PromptNode', () => {
  // Skipping this test - it needs to be rewritten after the conversion
  // to the tab based interface.
  it.skip('should allow you to edit the prompt on a node and have it recompute', () => {
    cy.visit(testChartAppUrl);

    const scrollWrapperElement = getPromptElement("3", ".current-value-scroll-wrapper");
    scrollWrapperElement.click();

    const editorElement = getPromptElement("3", ".node-custom-prompt-editor");
    // editorElement.clear();
    editorElement.type("test_prompt_value_NodFabDaic9Ot");

    // Find the save button and click that
    const saveButton = getPromptElement("3", ".save-action-button");
    saveButton.click();

    // Next lets check to see that we have the current value show up.
    const currentValueElement = getPromptElement("3", ".current-value-container");

    // Check that the span count shows several words, indicating the current value has come in
    currentValueElement.find("span").should("have.length.greaterThan", 0);
  })
})

