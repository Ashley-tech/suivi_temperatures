<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title>Suivi thermique</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-modal :is-open="isTemperatureFormOpen" @didDismiss="closeTemperatureForm">
        <ion-content class="ion-padding">
        <form class="temperature-form">
          <ion-item>
            <ion-label position="stacked">Valeur en degré (°C)*</ion-label>
            <ion-input v-model="newTemperature.degre" type="number" step="0.1" placeholder="Ex. 21.5" />
          </ion-item>

          <ion-item>
            <ion-label position="stacked">Localisation*</ion-label>
            <ion-select v-model="newTemperature.localisation" placeholder="Choisis une localisation">
              <ion-select-option v-for="location in locations" :key="location" :value="location">
                {{ location }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <ion-item>
            <ion-label position="stacked">Date de la température</ion-label>
            <ion-input v-model="newTemperature.date_temperature" type="date" />
          </ion-item>

          <ion-item>
            <ion-label position="stacked">Heure de la température</ion-label>
            <ion-input v-model="newTemperature.heure" type="time" />
          </ion-item>

          <div class="form-actions">
            <ion-button type="button" fill="outline" @click="closeTemperatureForm">Annuler</ion-button>
            <ion-button type="button" class="primary-action" @click="submitTemperature">Enregistrer</ion-button>
          </div>
        </form>
      </ion-content>
    </ion-modal>

    <ion-content :fullscreen="true" class="ion-padding">
      <main class="temperatures-container">
        <div class="page-heading">
          <h1>Ta liste de températures</h1>
          <p class="intro">Retrouve ici toutes les températures enregistrées sur ton compte.</p>
        </div>

        <div v-if="loading" class="state-message" role="status">
          Chargement de tes températures...
        </div>

        <div v-else-if="errorMessage" class="state-message error-message" role="alert">
          {{ errorMessage }}
        </div>

        <div v-else-if="temperatures.length === 0" class="state-message">
          Tu n'as encore aucune température enregistrée.
        </div>

        <div v-else class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th scope="col">Date</th>
                <th scope="col">Heure</th>
                <th scope="col">Température</th>
                <th scope="col">Localisation</th>
                <th scope="col" class="actions-heading">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="temperature in temperatures" :key="temperature.id">
                <td data-label="Date">{{ formatDate(temperature.date_temperature) }}</td>
                <td data-label="Heure">{{ formatTime(temperature.heure) }}</td>
                <td data-label="Température" class="temperature-value">{{ temperature.degre }} °C</td>
                <td data-label="Localisation">{{ temperature.localisation }}</td>
                <td data-label="Actions" class="actions-cell">
                  <ion-button fill="outline" size="small">Modifier</ion-button>
                  <ion-button fill="clear" color="danger" size="small" @click="confirmDeleteTemperature(temperature.id)">Supprimer</ion-button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="page-actions">
          <ion-button class="primary-action" @click="openTemperatureForm">
            Enregistrer une nouvelle température
          </ion-button>
          <ion-button fill="outline" @click="retour">Retour</ion-button>
        </div>
      </main>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import {useRouter} from "vue-router"
import Cookies from 'js-cookie';
import {
  IonButton,
  IonContent,
  IonHeader,
  IonButtons,
  IonInput,
  IonItem,
  IonPage,
  IonModal,
  IonLabel,
  IonSelect,
  IonSelectOption,
  IonTitle,
  IonToolbar,
  alertController,
} from '@ionic/vue';

interface Temperature {
  id: number;
  degre: number;
  localisation: string;
  date_temperature: string;
  heure: string | null;
}

const temperatures = ref<Temperature[]>([]);
const loading = ref(true);
const errorMessage = ref('');
const router = useRouter()
const isTemperatureFormOpen = ref(false);
const locations = ['NO', 'N', 'NE', 'SO', 'S', 'SE'];
const newTemperature = ref({
  degre: '',
  localisation: '',
  date_temperature: '',
  heure: '',
});
const compteId = Cookies.get("compte_id")

const loadTemperatures = async () => {
  const accessToken = sessionStorage.getItem('access_token');

  if (!compteId || !accessToken) {
    errorMessage.value = 'Ta session est introuvable. Reconnecte-toi pour voir tes températures.';
    loading.value = false;
    router.back()
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/temperatures/compte/${compteId}`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        typeof errorData?.detail === 'string'
          ? errorData.detail
          : 'Impossible de charger tes températures.',
      );
    }

    temperatures.value = await response.json();
  } catch (error) {
    errorMessage.value = error instanceof Error
      ? error.message
      : 'Le serveur est inaccessible. Vérifie qu\'il est démarré, puis réessaie.';
      if (errorMessage.value == "Token invalide ou expiré") {
        await logout()
      }
  } finally {
    loading.value = false;
  }
};

const logout = async () => {
  try {
    await fetch('http://127.0.0.1:8000/logout', {
      method: 'POST',
      credentials: 'include',
    });
  } finally {
    Cookies.remove('compte_id');
    Cookies.remove('email');
    sessionStorage.removeItem('access_token');
    await router.replace('/');
  }
};

const formatDate = (date: string) => new Intl.DateTimeFormat('fr-FR').format(new Date(`${date}T00:00:00`));

const formatTime = (time: string | null) => time ? time.slice(0, 5) : 'Non renseignée';

onMounted(loadTemperatures);



function openTemperatureForm() {
  isTemperatureFormOpen.value = true;
  newTemperature.value.degre = ""
  newTemperature.value.localisation = ""
  newTemperature.value.date_temperature = ""
  newTemperature.value.heure = ""
}

function closeTemperatureForm() {
  isTemperatureFormOpen.value = false;
}

function retour() {
    router.back()
}

const confirmDeleteTemperature = async (temperature_id: number) => {
  const alert = await alertController.create({
    header: 'Suppression',
    message: `Veux-tu vraiment supprimer la température (ID : ${temperature_id}) ?`,
    buttons: [
      { text: 'Oui', role: 'confirm' },
      { text: 'Non', role: 'cancel' },
    ],
  });

  await alert.present();
  const { role } = await alert.onDidDismiss();
  if (role === 'confirm') {
    await deleteTemperature(temperature_id)
  }
};

const deleteTemperature = async (temperature_id: number) => {
    const accessToken = sessionStorage.getItem("access_token")
    try {
  const response = await fetch(`http://127.0.0.1:8000/temperatures/${temperature_id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
        await showAlert(
        'Erreur',
        'La température n\'a pas pu être supprimée.',
        );
      throw new Error(
        typeof data?.detail === 'string'
          ? data.detail
          : 'La température n\'a pas pu être supprimée.',
      );
    }

    temperatures.value = temperatures.value.filter(
        temperature => temperature.id !== temperature_id
    );
    await showAlert('Succès', 'La température a bien été enregistrée.');

    console.log('Température créée par le backend :', data);
  } catch (error) {
    await showAlert(
      'Erreur',
      error instanceof Error ? error.message : 'Le serveur est inaccessible.',
    );
  }
}

const submitTemperature = async () => {
  const degre = newTemperature.value.degre;
  const localisation = newTemperature.value.localisation;
  var date = newTemperature.value.date_temperature;
  var heure = newTemperature.value.heure;
  const accessToken = sessionStorage.getItem('access_token');

  console.log('Degré :', degre);
  console.log('Localisation :', localisation);
  console.log('Date :', date);
  console.log('Heure :', heure);

  if (degre == "" ||localisation == ""){
    await showAlert('Champs manquants', 'Veuillez remplir tous les champs avant de sauvegarder vos informations.');
    return
  }

  const maintenant = new Date();

  // Si aucune date n'est renseignée → date actuelle
  if (date === "") {
    date = maintenant.toISOString().split('T')[0];
  }

  // Si aucune heure n'est renseignée → heure actuelle
  if (heure === "") {
    heure = maintenant.toTimeString().slice(0, 5);
  }

  // Exemple : objet contenant toutes les données
  const temperature = {
    degre,
    localisation,
    date_temperature: date,
    heure,
    compte_id: compteId
  };
  try {
  const response = await fetch(`http://127.0.0.1:8000/temperatures`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(temperature),
      credentials: 'include',
    });

    const data = await response.json();

    if (!response.ok) {
        await showAlert(
        'Erreur',
        'La température n\'a pas pu être enregistrée.',
        );
      throw new Error(
        typeof data?.detail === 'string'
          ? data.detail
          : 'La température n\'a pas pu être enregistrée.',
      );
    }

    temperatures.value.unshift(data);
    closeTemperatureForm();
    await showAlert('Succès', 'La température a bien été enregistrée.');

    console.log('Température créée par le backend :', data);
  } catch (error) {
    await showAlert(
      'Erreur',
      error instanceof Error ? error.message : 'Le serveur est inaccessible.',
    );
  }
}

const showAlert = async (header: string, message: string, buttons: string[] = ['OK']) => {
    const alert = await alertController.create({
      header: header,
      message: message,
      buttons: buttons
    });

    await alert.present();
  }
</script>

<style scoped>
.temperatures-container {
  width: min(1180px, 100%);
  margin: 0 auto;
  padding: 28px 8px 36px;
}

.page-heading {
  margin-bottom: 28px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #0f766e;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  color: #12343b;
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 750;
}

.intro {
  margin: 10px 0 0;
  color: #52666b;
  font-size: 1rem;
}

.state-message {
  padding: 34px 20px;
  border: 1px solid #d6e4e2;
  border-radius: 8px;
  background: #f7fbfa;
  color: #52666b;
  text-align: center;
}

.error-message {
  border-color: #f0c7c7;
  background: #fff7f7;
  color: #a33a3a;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid #d6e4e2;
  border-radius: 8px;
  background: #ffffff;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 720px;
}

th,
td {
  padding: 16px 18px;
  border-bottom: 1px solid #e6eeee;
  text-align: left;
  white-space: nowrap;
}

th {
  background: #edf6f4;
  color: #31545a;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

td {
  color: #29454b;
}

tbody tr:last-child td {
  border-bottom: 0;
}

.temperature-value {
  color: #0f766e;
  font-weight: 700;
}

.actions-heading,
.actions-cell {
  text-align: right;
}

.actions-cell ion-button {
  margin: 0 0 0 6px;
}

.page-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.page-actions ion-button {
  margin: 0;
}

.primary-action {
  --background: #0f766e;
  --background-hover: #0b5f59;
}

.temperature-form {
  width: min(520px, 100%);
  margin: 0 auto;
}

.temperature-form ion-item {
  margin-bottom: 14px;
  --padding-start: 0;
  --inner-padding-end: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 28px;
}

.form-actions ion-button {
  margin: 0;
}

@media (max-width: 600px) {
  .temperatures-container {
    padding-inline: 0;
  }

  .page-actions {
    justify-content: stretch;
  }

  .page-actions ion-button {
    flex: 1 1 100%;
  }
}
</style>
