<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useValidation } from '@/composables/validation'

const authStore = useAuthStore()
const router = useRouter()
const val = useValidation()
const userStore = useUserStore()
const errorMessage = ref('')
const confirmPassword = ref('')
const route = useRoute()

const user = ref({
  name: '',
  surname: '',
  birthDate: '',
  gender: '',
  password: '',
  confirmPassword: ''
})

const localizedText = ref({
  login: '',
  register: '',
  name: '',
  surname: '',
  password: '',
  namerequired: '',
  surnamerequired: '',
  genderrequired: '',
  birthdaterequired: '',
  passwordrequired: '',
  passwordsmismatch: '',
  gender: '',
  birthdate: '',
  agerequired: '',
  condition: '',
  select: '',
  female: '',
  male: '',
  other: '',
  alzheimers: '',
  selectCondition: '',
  submit: '',
  alreadydiagnosed: '',
  conditionrequired: '', 
  confirmPassword: ''
})


// Localization method
async function getLocalization(defaultText, key) {
  try {
    const response = await fetch('/api/test/getlocalization', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'language': sessionStorage.getItem('language')
      },
      body: JSON.stringify({ default: defaultText })
    })

    if (response.ok) {
      const result = await response.json()
      localizedText.value[key] = result.translation
    } else {
      console.error('Failed to fetch localization')
    }
  } catch (error) {
    console.error('Error fetching localization:', error)
  }
}

onMounted(() => {
  getLocalization('Login', 'login')
  getLocalization('Register', 'register')
  getLocalization('Name', 'name')
  getLocalization('Surname', 'surname')
  getLocalization('Password', 'password'),
  getLocalization('Name is required.', 'namerequired'),
  getLocalization('Surname is required.', 'surnamerequired'),
  getLocalization('Gender is required.', 'genderrequired'),
  getLocalization('Birthdate is required.', 'birthdaterequired'),
  getLocalization('Password is required.', 'passwordrequired'),
  getLocalization('Passwords do not match.', 'passwordsmismatch'),
  getLocalization('Gender', 'gender'),
  getLocalization('Birthday -- Date of birth', 'birthdate'),
  getLocalization('You must be at least 18 years old.', 'agerequired')
  getLocalization('Select Condition', 'condition'),
  getLocalization('Select...', 'select'),
  getLocalization('Female', 'female'),
  getLocalization('Male', 'male'),
  getLocalization('Other', 'other'),
  getLocalization('Alzheimer`s', 'alzheimers'),
  getLocalization('Please select a condition', 'selectCondition'),
  getLocalization('Submit', 'submit'),
  getLocalization('Are you already diagnosed with this condition?', 'alreadydiagnosed'),
  getLocalization('Condition is required.', 'conditionrequired'),
  getLocalization('Confirm Password', 'confirmPassword')
  user.value.name = route.query.name || ''
  user.value.surname = route.query.surname || ''
})

const hasAttemptedSubmit = ref(false)
const isNameEmpty = computed(() => hasAttemptedSubmit.value && user.value.name === '')
const isSurnameEmpty = computed(() => hasAttemptedSubmit.value && user.value.surname === '')
const isGenderEmpty = computed(() => hasAttemptedSubmit.value && user.value.gender === '')
const isBirthDateEmpty = computed(() => hasAttemptedSubmit.value && user.value.birthDate === '')
const isPasswordEmpty = computed(() => hasAttemptedSubmit.value && user.value.password === '')
const isConditionEmpty = computed(() => hasAttemptedSubmit.value && selectedCondition.value === '')
const isPasswordMismatch = computed(
  () => hasAttemptedSubmit.value && !matchPasswords(user.value.password, confirmPassword.value)
)

const selectedCondition = ref('')
/*function isPasswordSecure(password) {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return regex.test(password);
}*/

const matchPasswords = (password1, password2) => {
  return password1 === password2
}

const createUser = async () => {
  hasAttemptedSubmit.value = true // Indicate submission attempt
  if (
    isNameEmpty.value ||
    isSurnameEmpty.value ||
    isGenderEmpty.value ||
    isBirthDateEmpty.value ||
    isPasswordEmpty.value ||
    isConditionEmpty.value ||
    isPasswordMismatch.value
  ) {
    errorMessage.value = 'Please fill in all fields.'
    return
  }
  const passwordFeedback = val.isPasswordSecure(user.value.password)
  const passwordField = document.getElementById('pw-field')
  if (passwordFeedback) {
    errorMessage.value =
      'Password does not meet security requirements: ' + passwordFeedback.join(' ')
    if (passwordField) {
      passwordField.classList.add('is-invalid')
    } else {
      if (passwordField) {
        passwordField.classList.remove('is-invalid')
      }
    }
    return
  }
  if (birthdayError.value) {
    return
  }

  try {
    const response = await fetch('/api/user/create_patient', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user.value)
    })

    if (!response.ok) {
      throw new Error('Failed to create user')
    }

    const data = await response.json()
    userStore.setSessionId(data.session_id)
    sessionStorage.setItem('session_id', data.session_id)
    sessionStorage.setItem('name', user.value.name)
    sessionStorage.setItem('surname', user.value.surname)
    authStore.updateAuthStatus(true)
    router.push('/')
  } catch (error) {
    errorMessage.value = error.message
  }
}
const birthdayError = computed(() => {
  if (!user.value.birthDate) return false
  var birthday = new Date(user.value.birthDate)
  const today = new Date()
  var age = today.getFullYear() - birthday.getFullYear()
  const m = today.getMonth() - birthday.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birthday.getDate())) {
    age--
  }
  return age < 18
})
</script>

<template>
  <div class="container login-container" id="mainContent">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ localizedText.register || 'Register' }}</h5>
            <form @submit.prevent="createUser" class="login-form">
              <div class="mb-3">
                <label for="name" class="form-label">{{ localizedText.name || 'Name' }}</label>
                <input
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': isNameEmpty }"
                  id="name"
                  v-model="user.name"
                />
                <div v-if="isNameEmpty" class="invalid-feedback">{{ localizedText.namerequired || 'Name is required.' }}</div>
              </div>
              <div class="mb-3">
                <label for="surname" class="form-label">{{ localizedText.surname || 'Surname' }}</label>
                <input
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': isSurnameEmpty }"
                  id="surname"
                  v-model="user.surname"
                />
                <div v-if="isSurnameEmpty" class="invalid-feedback">{{ localizedText.surnamerequired || 'Surname is required.' }}</div>
              </div>
              <div class="mb-3">
                <label for="gender" class="form-label">{{ localizedText.gender || 'Gender' }}</label>
                <select
                  class="form-select"
                  :class="{ 'is-invalid': isGenderEmpty }"
                  id="gender"
                  v-model="user.gender"
                >
                  <option value="">{{ localizedText.select || 'Select...' }}</option>
                  <option value="female">{{ localizedText.female || 'Female' }}</option>
                  <option value="male">{{ localizedText.male || 'Male' }}</option>
                  <option value="other">{{ localizedText.other || 'Other' }}</option>
                </select>
                <div v-if="isGenderEmpty" class="invalid-feedback">{{ localizedText.genderrequired || 'Gender is required.' }}</div>
              </div>
              <div class="mb-3">
                <label for="birthDate" class="form-label">{{ localizedText.birthdate || 'Birthday' }}</label>
                <input
                  type="date"
                  class="form-control"
                  :class="{ 'is-invalid': isBirthDateEmpty }"
                  id="birthDate"
                  v-model="user.birthDate"
                />
                <div v-if="isBirthDateEmpty" class="invalid-feedback">{{ localizedText.birthdaterequired || 'Birthdate is required.' }}</div>
                <div v-if="birthdayError" class="form-text text-danger">
                  {{ localizedText.agerequired || 'You must be at least 18 years old.' }}
                </div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">{{ localizedText.password || 'Password' }}</label>
                <input
                  id="pw-field"
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': isPasswordEmpty }"
                  v-model="user.password"
                  placeholder="Password"
                  required
                />
                <div v-if="isPasswordEmpty" class="invalid-feedback">{{ localizedText.passwordrequired || 'Password is required.' }}</div>
                <div v-if="errorMessage" class="invalid-feedback">
                  {{ errorMessage }}
                </div>
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">{{ localizedText.confirmPassword || 'Confirm Password' }}</label>
                <input
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': isPasswordMismatch }"
                  id="confirmPassword"
                  v-model="confirmPassword"
                />
                <div v-if="isPasswordMismatch" class="invalid-feedback">
                  {{ localizedText.passwordsmismatch || 'Passwords do not match.' }}
                </div>
              </div>
              <div class="section mb-3">
                <label for="condition" class="form-label">{{ localizedText.condition || 'Select Condition' }}</label>
                <select
                  class="form-select"
                  :class="{ 'is-invalid': isConditionEmpty }"
                  id="condition"
                  v-model="selectedCondition"
                >
                  <option disabled value="">{{ localizedText.selectCondition || 'Please select a condition' }}</option>
                  <option value="alzheimers">{{ localizedText.alzheimers || 'Alzheimer\`s' }}</option>
                  <!--<option value="parkinsons">Parkinson</option>-->
                </select>
                <div v-if="isConditionEmpty" class="invalid-feedback">{{ localizedText.conditionrequired || 'Condition is required.' }}</div>
                <div class="form-check mb-3 conditionalElement" v-if="selectedCondition">
                  <input class="form-check-input" type="checkbox" value="" id="diagnosedCheck" />
                  <label class="form-check-label" for="diagnosedCheck">
                    {{ localizedText.alreadydiagnosed || 'Are you already diagnosed with this condition?' }}  
                  </label>
                </div>
              </div>
              <button type="submit" class="btn btn-primary">{{ localizedText.submit || 'Submit' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
/* Add your styles here */
.btn {
  margin-right: 1em;
}
</style>
