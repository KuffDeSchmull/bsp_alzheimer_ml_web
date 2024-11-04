describe('Navigation to Input Page from Home', () => {
  it('Logs in and navigates to the Input page by clicking TestListItem', () => {
    // Use the custom login command
    cy.login('Max', 'Mustermann', 'Password123!');

    // After login, verify redirection to the home page
    cy.url().should('include', '/');

    // Wait for the test list items to be loaded
    cy.get('.tests-list li', { timeout: 10000 }).should('have.length.greaterThan', 0);

    cy.get('.tests-list li').first().find('button').click();

    // Verify redirection to the /input page with appropriate query parameters
    cy.url().should('include', '/input?testName=Clock+Drawing+Test&testType=cdt&taskCount=1');
    cy.get('button').contains('Paper Drawing').click();
    cy.url().should('include', '/draw');
    cy.get('button').contains('Start').click();
    cy.get('button').contains('Stop').click();
    cy.get('button').contains('Next').click();
    cy.url().should('include', '/import');
    cy.get('button').contains('Import Image').click();

    // Select and upload the image file
    cy.get('input[type="file"]').first().selectFile('cypress/fixtures/clock1.png', { force: true });

   

    // Wait for the image to be processed
    cy.wait(5000);
    cy.get('.cropper-image', { timeout: 10000 }).should('be.visible');

    // Click on the button to send the image
    cy.get('button').contains('Send Image').click({ force: true });
    cy.url().should('include', '/results');

  });
});
