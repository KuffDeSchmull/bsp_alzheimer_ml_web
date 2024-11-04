import { defineStore } from 'pinia'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    prename: '', //initial value
    surname: '',
    gender: '',
    birthDate: '',
    sessionID: ''
  }),
  actions: {
    createProfile(prename, surname, gender, birthDate) {
      this.prename = prename
      this.surname = surname
      this.gender = gender
      this.birthdate = new Date(birthDate)
    },
    clearProfile() {
      this.prename = ''
      this.surname = ''
      this.gender = ''
      this.birthDate = ''
      // Additional actions like redirecting
    },
    updateName(pre, sur) {
      this.prename = pre
      this.surname = sur
    },
    updateGender(gender) {
      this.gender = gender
    },
    updateBirthDate(bd) {
      this.birthDate = new Date(birthDate)
    }
  }
})
