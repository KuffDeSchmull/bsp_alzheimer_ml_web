describe('Registration Test', () => {
  it('Successfully register a new user', () => {
    cy.visit('/register'); //registration route
    // Input fields
    cy.get('input#name').type('Max'); // Input for 'Name'
    cy.get('input#surname').type('Mustermann'); // Input for 'Surname'
    cy.get('select#gender').select('Male'); // Select for 'Gender'
    cy.get('input#birthDate').type('1990-01-01'); // Input for 'BirthDate'
    cy.get('input#pw-field').type('Password123!'); // Input for 'Password'
    cy.get('input#confirmPassword').type('Password123!'); // Input for 'Confirm Password'
    cy.get('select#condition').select('alzheimers'); // Select for 'Condition'

    // Submitting the form
    cy.get('form').submit();
    cy.url().should('include', '/');
  });
});