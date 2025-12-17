const urlInput = document.getElementById("urlInput");
const fetchBtn = document.getElementById("fetchBtn");
const loading = document.getElementById("loading");
const resultArea = document.getElementById("resultArea");
const thumbnail = document.getElementById("thumbnail");
const videoTitle = document.getElementById("videoTitle");
const typeSelect = document.getElementById("typeSelect");
const qualitySelect = document.getElementById("qualitySelect");
const downloadBtn = document.getElementById("downloadBtn");
const statusMessage = document.getElementById("statusMessage");

let currentVideoInfo = null;

const checkUpdateBtn = document.getElementById("checkUpdateBtn");

fetchBtn.addEventListener("click", fetchInfo);

const updateModal = document.getElementById("updateModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const confirmUpdateBtn = document.getElementById("confirmUpdateBtn");
const modalTitle = document.getElementById("modalTitle");
const modalMessage = document.getElementById("modalMessage");

let updateUrl = "";


let updateVersion = "";

// Auto-check on load
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/check-update");
    const data = await response.json();
    
    if (data.update_available) {
      updateUrl = data.download_url;
      updateVersion = data.latest_version;
      checkUpdateBtn.classList.remove("hidden");
    }
  } catch (error) {
    console.error("Error al verificar actualizaciones:", error);
  }
});

checkUpdateBtn.addEventListener("click", () => {
  if (updateUrl) {
    showModal("Actualización Disponible", `Nueva versión ${updateVersion} está disponible.`);
    confirmUpdateBtn.classList.remove("hidden");
  }
});

closeModalBtn.addEventListener("click", () => {
  updateModal.classList.add("hidden");
});

confirmUpdateBtn.addEventListener("click", async () => {
  if (updateUrl) {
    confirmUpdateBtn.disabled = true;
    confirmUpdateBtn.textContent = "Descargando e Instalando...";
    
    try {
      const response = await fetch("/api/update", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ download_url: updateUrl })
      });
      
      const res = await response.json();
      if (!response.ok) throw new Error(res.detail || "Update failed");
      
      showStatus("Actualización descargada. El programa se reiniciará...", "success");
      // The backend will exit, so we might want to close or show a final message.
    } catch (error) {
       console.error(error);
       showStatus("Error al actualizar: " + error.message, "error");
       confirmUpdateBtn.disabled = false;
       confirmUpdateBtn.textContent = "Sí, Actualizar";
    }
  }
});

function showModal(title, message) {
  modalTitle.textContent = title;
  modalMessage.textContent = message;
  updateModal.classList.remove("hidden");
}
urlInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") fetchInfo();
});

async function fetchInfo() {
  const url = urlInput.value.trim();
  if (!url) return;

  showLoading(true);
  hideResult();
  hideStatus();

  try {
    const response = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
    if (!response.ok) throw new Error("Error al obtener información del video");

    const data = await response.json();
    currentVideoInfo = data;
    displayInfo(data);
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    showLoading(false);
  }
}

function displayInfo(data) {
  thumbnail.src = data.thumbnail;
  videoTitle.textContent = data.title;

  updateQualityOptions();
  resultArea.classList.remove("hidden");
}

typeSelect.addEventListener("change", updateQualityOptions);

function updateQualityOptions() {
  if (!currentVideoInfo) return;

  const type = typeSelect.value;
  qualitySelect.innerHTML = "";

  const options = currentVideoInfo.formats.filter((f) => f.type === type);

  options.forEach((opt) => {
    const el = document.createElement("option");
    el.value = opt.format_id;
    el.textContent = opt.quality;
    qualitySelect.appendChild(el);
  });
}

downloadBtn.addEventListener("click", async () => {
  if (!currentVideoInfo) return;

  const url = urlInput.value.trim();
  const format_id = qualitySelect.value;
  const type = typeSelect.value;

  downloadBtn.disabled = true;
  downloadBtn.textContent = "Descargando...";
  hideStatus();

  try {
    const response = await fetch("/api/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
        format_id: format_id,
        type: type,
      }),
    });

    if (!response.ok) throw new Error("Error al descargar");

    const result = await response.json();
    showStatus("Descarga completada! Guardado en la carpeta de descargas.", "success");
  } catch (error) {
    showStatus(
      "Error al descargar video. Asegúrate de tener ffmpeg instalado si estás convirtiendo.",
      "error"
    );
  } finally {
    downloadBtn.disabled = false;
    downloadBtn.textContent = "Descargar";
  }
});

function showLoading(show) {
  if (show) loading.classList.remove("hidden");
  else loading.classList.add("hidden");
}

function hideResult() {
  resultArea.classList.add("hidden");
}

function showStatus(msg, type) {
  statusMessage.textContent = msg;
  statusMessage.classList.remove("hidden");
  statusMessage.style.color = type === "error" ? "#ff4444" : "#00ff60";
  statusMessage.style.background =
    type === "error" ? "rgba(255, 68, 68, 0.1)" : "rgba(0, 255, 100, 0.1)";
  statusMessage.style.borderColor =
    type === "error" ? "rgba(255, 68, 68, 0.2)" : "rgba(0, 255, 100, 0.2)";
}

function hideStatus() {
  statusMessage.classList.add("hidden");
}
