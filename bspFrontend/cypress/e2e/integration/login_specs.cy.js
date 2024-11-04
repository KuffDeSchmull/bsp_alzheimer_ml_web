describe('Login Test', () => {
    it('Successfully logs in', () => {
      cy.visit('/login'); // Navigate to the login route
      cy.get('input#loginName').type('Max'); // Input for 'Name'
      cy.get('input#loginSurname').type('Mustermann'); // Input for 'Surname'
      cy.get('input#loginPassword').type('Password123!'); // Input for 'Password'
      cy.get('form').submit(); // Submit the form
      cy.url().should('include', '/'); // Assuming successful login redirects to the home page ('/')
    });
  });
  