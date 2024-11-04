<template>
  <div class="container my-4" id="mainContent">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">{{ localizedText.settings || 'Settings' }}</h2>
            <div class="settings mt-4">
              <div class="d-grid gap-2">
                <button @click="clearLocalStorage" class="btn btn-danger">{{ localizedText.logOut || 'Log Out' }}</button>
                <button @click="deleteAccount" class="btn btn-warning">{{ localizedText.deleteAccount || 'Delete Account' }}</button>
                <label for="lang-select">{{ localizedText.chooseYourLanguage || 'Choose your language:' }}</label>
                <select class="btn btn-warning" name="languages" id="lang-select" @change="changeLanguage">
                  <option value="">{{ localizedText.chooseLanguage || 'Choose Language' }}</option>
                  <option value="">{{ localizedText.english || 'English' }}</option>
                  <option value="esp">{{ localizedText.spanish || 'Spanish/ Espagnol' }}</option>
                </select>
                <!-- Toggle for Large Font -->
                <div class="form-check form-switch ltoggle first-toggle">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="largeFontToggle"
                    :checked="accessibilityStore.useLargeFont"
                    @change="toggleLargeFont"
                  />
                  <label class="form-check-label toggle-label" for="largeFontToggle"
                    >{{ localizedText.largeFont || 'Large Font' }}</label
                  >
                </div>

                <!-- Toggle for Serif Font -->
                <div class="form-check form-switch ltoggle">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="serifFontToggle"
                    :checked="accessibilityStore.useSerifFont"
                    @change="toggleSerifFont"
                  />
                  <label class="form-check-label toggle-label" for="serifFontToggle"
                    >{{ localizedText.serifFont || 'Serif Font' }}</label
                  >
                </div>

                <!-- Toggle for High Contrast -->
                <div class="form-check form-switch ltoggle">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="highContrastToggle"
                    :checked="accessibilityStore.highContrast"
                    @change="toggleHighContrast"
                  />
                  <label class="form-check-label toggle-label" for="highContrastToggle"
                    >{{ localizedText.highContrast || 'High Contrast' }}</label
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useAccessibilityStore } from '@/stores/settings'

export default {
  data() {
    return {
      localizedText: {
        largeFont: null,
        serifFont: null,
        highContrast: null,
        logOut: null,
        deleteAccount: null,
        chooseYourLanguage: null,
        chooseLanguage: null,
        english: null,
        spanish: null,
        settings: null
      }
    }
  },
  mounted() {
    // Fetch initial localization for the current UI elements
    this.getLocalization('Large Font', 'largeFont')
    this.getLocalization('Serif Font', 'serifFont')
    this.getLocalization('High Contrast', 'highContrast')
    this.getLocalization('Log Out', 'logOut')
    this.getLocalization('Delete Account', 'deleteAccount')
    this.getLocalization('Choose your language', 'chooseYourLanguage')
    this.getLocalization('Choose Language', 'chooseLanguage')
    this.getLocalization('English', 'english')
    this.getLocalization('Spanish', 'spanish')
    this.getLocalization('Settings', 'settings')
  },
  setup() {
    const accessibilityStore = useAccessibilityStore()

    const toggleLargeFont = () => {
      accessibilityStore.toggleLargeFont()
      console.log(accessibilityStore.useLargeFont)
    }

    const toggleSerifFont = () => {
      accessibilityStore.toggleSerifFont()
    }
    const toggleHighContrast = () => {
      accessibilityStore.toggleHighContrast()
    }

    return {
      accessibilityStore,
      toggleLargeFont,
      toggleSerifFont,
      toggleHighContrast
    }
  },
  methods: {
    clearLocalStorage() {
      // Clearing the local storage
      const authStore = useAuthStore()
      authStore.clearLocalStorageAndLogout()
      this.$router.push('/login')
    },
    async deleteAccount() {
      const name = sessionStorage.getItem('name')
      const surname = sessionStorage.getItem('surname')
      console.log(surname)
      try {
        const response = await fetch('/api/user/delete_user', {
          method: 'DELETE',
          headers: {
            Name: name,
            Surname: surname
          }
        })

        if (!response.ok) {
          throw new Error('Failed to delete account')
        }

        // Clear local storage and redirect to login
        this.clearLocalStorage()
      } catch (error) {
        console.error('Error:', error)
        // Handle the error (e.g., show an alert to the user)
      }
    },
    changeLanguage(event) {
      const selectedLanguage = event.target.value
      sessionStorage.setItem('language', selectedLanguage)
      console.log('Language saved:', selectedLanguage)
      location.reload()
    },
    async getLocalization(defaultText, key) {
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
          this.localizedText[key] = result.translation
        } else {
          console.error('Failed to fetch localization')
        }
      } catch (error) {
        console.error('Error fetching localization:', error)
      }
    }
  }
}
</script>

<style>
.ltoggle .form-check-input {
  width: 4em;
  height: 2em;
  cursor: pointer;
}

.ltoggle .form-check-input::before {
  width: 2.5em;
  height: 2.5em;
}
.toggle-label {
  font-size: 1.5em; /* Larger font size */

  margin-left: 0.5em; /* Adjust spacing between toggle and label */
}
.first-toggle {
  margin-top: 1.5em;
}
</style>
