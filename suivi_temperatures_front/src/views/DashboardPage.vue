<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-title>Suivi thermique</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content :fullscreen="true">
      <main class="container">
        <h2>Températures récentes</h2>

        <p v-if="loading" class="message">Chargement des températures...</p>
        <p v-else-if="temperatures.length === 0" class="message">
          Aucune température enregistrée.
        </p>

        <section v-else class="chart-card" aria-label="Graphique des quatre dernières températures">
          <svg class="temperature-chart" viewBox="0 0 640 320" role="img">
            <line x1="56" y1="24" x2="56" y2="260" class="axis" />
            <line x1="56" y1="260" x2="616" y2="260" class="axis" />
            <polyline :points="chartPoints" class="chart-line" />
            <g v-for="point in chartData" :key="point.id">
              <circle :cx="point.x" :cy="point.y" r="6" class="chart-point" />
              <text :x="point.x" y="286" text-anchor="middle" class="chart-label">
                {{ point.label }}
              </text>
              <text :x="point.x" :y="point.y - 14" text-anchor="middle" class="chart-value">
                {{ point.value }}°
              </text>
            </g>
          </svg>
        </section>

        <ion-button expand="block" fill="outline">
          Liste de toutes vos températures
        </ion-button>
        <ion-button expand="block" fill="outline">
          Modifier vos informations
        </ion-button>
        <ion-button expand="block" fill="outline" @click="confirmLogout">
          Se déconnecter
        </ion-button>
      </main>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import Cookies from 'js-cookie';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  alertController,
  IonButton,
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
} from '@ionic/vue';

interface Temperature {
  id: number;
  degre: number | string;
  date_temperature: string;
  heure?: string | null;
}

interface ChartPoint {
  id: number;
  x: number;
  y: number;
  value: number;
  label: string;
}

const router = useRouter();
const temperatures = ref<Temperature[]>([]);
const loading = ref(true);

const showError = async (message: string) => {
  const alert = await alertController.create({
    header: 'Chargement impossible',
    message,
    buttons: ['OK'],
  });
  await alert.present();
};

const logout = async () => {
  try {
    await fetch('http://127.0.0.1:8000/login/logout', {
      method: 'POST',
      credentials: 'include',
    });
  } finally {
    Cookies.remove('compte_id');
    Cookies.remove('email');
    sessionStorage.removeItem('access_token');
    await router.push('/');
  }
};

const confirmLogout = async () => {
  const alert = await alertController.create({
    header: 'Déconnexion',
    message: 'Voulez-vous vraiment vous déconnecter ?',
    buttons: [
      { text: 'Non', role: 'cancel' },
      { text: 'Oui', role: 'confirm' },
    ],
  });

  await alert.present();
  const { role } = await alert.onDidDismiss();
  if (role === 'confirm') {
    await logout();
  }
};

const recentTemperatures = computed(() => temperatures.value.slice(0, 4).reverse());

const chartData = computed<ChartPoint[]>(() => {
  const values = recentTemperatures.value.map((temperature) => Number(temperature.degre));
  const minimum = Math.min(...values);
  const maximum = Math.max(...values);
  const range = Math.max(maximum - minimum, 1);

  return recentTemperatures.value.map((temperature, index) => {
    const value = Number(temperature.degre);
    const x = recentTemperatures.value.length === 1
      ? 336
      : 56 + (index * 560) / (recentTemperatures.value.length - 1);
    const y = 236 - ((value - minimum) / range) * 190;
    const date = new Date(`${temperature.date_temperature}T${temperature.heure ?? '00:00:00'}`);

    return {
      id: temperature.id,
      x,
      y,
      value,
      label: date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' }),
    };
  });
});

const chartPoints = computed(() => chartData.value.map((point) => `${point.x},${point.y}`).join(' '));

const loadTemperatures = async () => {
  const compteId = Cookies.get("compte_id");
  if (typeof compteId !== 'string' || !compteId) {
    loading.value = false;
    await showError('Identifiant du compte manquant. Reconnectez-vous.');
    return;
  }

  try {
    const accessToken = sessionStorage.getItem('access_token');
    const response = await fetch(`http://127.0.0.1:8000/temperatures/compte/${compteId}`, {
      headers: accessToken
        ? { Authorization: `Bearer ${accessToken}` }
        : undefined,
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      if (response.status === 401) {
        sessionStorage.removeItem('access_token');
      }
      throw new Error(typeof errorData?.detail === 'string' ? errorData.detail : 'Une erreur est survenue.');
    }

    temperatures.value = await response.json();
  } catch (error) {
    await showError(error instanceof Error ? error.message : 'Le serveur est inaccessible.');
  } finally {
    loading.value = false;
  }
};

onMounted(loadTemperatures);
</script>

<style scoped>
.container {
  max-width: 760px;
  margin: 0 auto;
  padding: 36px 20px;
}

h2 {
  margin: 0 0 24px;
  font-size: 1.5rem;
  text-align: center;
}

.message {
  color: #64748b;
  text-align: center;
}

.container > ion-button {
  margin-bottom: 24px;
}

.chart-card {
  width: 100%;
  overflow-x: auto;
  border: 1px solid #dbe4ee;
  border-radius: 8px;
  background: #ffffff;
  padding: 16px;
}

.temperature-chart {
  display: block;
  width: 100%;
  min-width: 520px;
  height: auto;
}

.axis {
  stroke: #94a3b8;
  stroke-width: 1;
}

.chart-line {
  fill: none;
  stroke: #0f766e;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 4;
}

.chart-point {
  fill: #ffffff;
  stroke: #0f766e;
  stroke-width: 4;
}

.chart-label,
.chart-value {
  fill: #475569;
  font-size: 14px;
}

.chart-value {
  fill: #0f766e;
  font-weight: 700;
}
</style>
