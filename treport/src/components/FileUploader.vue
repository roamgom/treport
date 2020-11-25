<template>
  <div>
    <div id="upload-file-field">
      <v-card id="uploader" max-width="800" max-height="400">
        <div
          @dragover="dragover"
          @dragleave="dragleave"
          @drop="drop"
        >
          <input
            type="file"
            name="fields[assetsFieldHandle][]"
            id="assetsFieldHandle"
            class="w-px h-px opacity-0 overflow-hidden absolute"
            @change="onChange"
            ref="file"
            accept=".csv"
            hidden
          />

          <label for="assetsFieldHandle" class="block cursor-pointer">
            <div id="file-form">
              과세거래 내역 CSV 파일을 드래그하거나
              <span class="underline">클릭</span>하여 파일을 업로드 해주세요.
            </div>
          </label>
          <ul class="mt-4" v-if="this.filelist.length" v-cloak>
            <li
              v-for="file in this.filelist"
              v-bind:key="filelist.indexOf(file)"
              class="text-sm p-1"
            >
              {{ file.name
              }}<button
                type="button"
                @click="remove(filelist.indexOf(file))"
                title="Remove file"
              >
                X
              </button>
            </li>
          </ul>
        </div>
      </v-card>
    </div>
    <div id="button">
      <v-btn
        :loading="loading3"
        :disabled="loading3"
        color="blue-grey"
        class="ma-2 white--text"
        @click="loader = 'loading3'; "
      >
        Upload
      </v-btn>
    </div>
    <div id="download-file-field">
      Download
    </div>
  </div>
</template>
<script>
export default {
  name: "FileUploader",
  data() {
    return {
      loader: null,
      loading: false,
      loading2: false,
      loading3: false,
      loading4: false,
      loading5: false,
      filelist: [],
      reportfile: null,
    };
  },
  methods: {
    onChange() {
      this.filelist = [...this.$refs.file.files];
    },
    remove(i) {
      this.filelist.splice(i, 1);
    },
    dragover(event) {
      event.preventDefault();
      // Add some visual fluff to show the user can drop its files
      if (!event.currentTarget.classList.contains("bg-green-300")) {
        event.currentTarget.classList.remove("bg-gray-100");
        event.currentTarget.classList.add("bg-green-300");
      }
    },
    dragleave(event) {
      // Clean up
      event.currentTarget.classList.add("bg-gray-100");
      event.currentTarget.classList.remove("bg-green-300");
    },
    drop(event) {
      event.preventDefault();
      this.$refs.file.files = event.dataTransfer.files;
      this.onChange(); // Trigger the onChange event manually
      // Clean up
      event.currentTarget.classList.add("bg-gray-100");
      event.currentTarget.classList.remove("bg-green-300");
      console.log(this.$refs.file.files[0]);
    },
    
  },
  watch: {
    loader() {
      const l = this.loader;
      this[l] = !this[l];

      setTimeout(() => (this[l] = false), 3000);

      this.loader = null;
    },
  },
};
</script>

<style scoped>
ul {
  list-style-type: none;
}

#uploader {
  height: 150px;
}
#file-form {
  height: 150px;
  padding-top: 10%;
  padding-bottom: 10%;
}
#upload-file-field {
  text-align: center;
  width: 500px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5px;
  margin-bottom: 10px;
}
#download-file-field {
}
</style>
