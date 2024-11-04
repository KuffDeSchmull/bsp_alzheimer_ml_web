export const useValidation = () => {
  const isPasswordSecure = (password) => {
    const requirements = [
      { test: /[a-z]/, message: 'Include at least one lowercase letter.' },
      { test: /[A-Z]/, message: 'Include at least one uppercase letter.' },
      { test: /\d/, message: 'Include at least one number.' },
      {
        test: /[@$!%*?&]/,
        message: 'Include at least one special character (@, $, !, %, *, ?, &).'
      },
      { test: /.{8,}/, message: 'Be at least 8 characters long.' }
    ]

    const failingTests = requirements.filter((req) => !req.test.test(password))
    return failingTests.length === 0 ? null : failingTests.map((req) => req.message)
  }

  return { isPasswordSecure }
}
