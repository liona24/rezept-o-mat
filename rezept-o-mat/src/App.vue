<template>
  <div class="container">
    <div>
      <h1 class="title">
        REZEPT-O-MAT
      </h1>
      <h2 class="subtitle">
        Rezepte für den Unentschlossenen
      </h2>
      <div class="content">
        <template v-if="isLoading">
          LOADING
        </template>
        <template v-else>
          <p>
            Wie wäre es heute mit
            <a :href="selectedRecipe.source" class="recipe-title">{{
              selectedRecipe.title
            }}</a
            >:
          </p>
          <table>
            <tbody>
              <tr
                v-for="(ing, index) in selectedRecipe.ingredients"
                v-bind:key="'ing' + index"
              >
                <td class="td-left">{{ ing[1] }}</td>
                <td class="td-right">{{ ing[0] }}</td>
              </tr>
            </tbody>
          </table>

          <div class="description">
            <p
              v-for="(line, index) in selectedRecipe.description"
              v-bind:key="'desc' + index"
            >
              {{ line }}
            </p>
          </div>
          <div>
            <button @click="reload" class="reload-btn">
              <span class="reload">&#x21bb;</span>
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { ENDPOINT_RECIPE } from "./api";
import axios from "axios";

export default {
  data() {
    return {
      isLoading: true,
      selectedRecipe: {
        id: null,
        title: null,
        ingredients: [],
        description: [],
        source: null
      }
    };
  },
  created() {
    this.reload();
  },
  methods: {
    reload() {
      this.isLoading = true;
      axios.get(ENDPOINT_RECIPE).then(resp => {
        const ids = resp.data.map(v => v.id);
        const selected = ids[Math.floor(Math.random() * ids.length)];
        axios.get(`${ENDPOINT_RECIPE}/${selected}`).then(resp => {
          this.selectedRecipe.id = resp.data.id;
          this.selectedRecipe.title = resp.data.title;
          this.selectedRecipe.ingredients = resp.data.ingredients;
          this.selectedRecipe.description = resp.data.description;
          this.selectedRecipe.source = resp.data.source;
          this.isLoading = false;
        });
      });
    }
  }
};
</script>

<style>
body {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  text-align: center;
  margin-top: 3em;
}
.content {
  max-width: 60em;
}
.title {
  display: block;
  font-weight: 300;
  font-size: 4.5em;
  color: #35495e;
  letter-spacing: 1px;
  margin-bottom: 0.2em;
}
.subtitle {
  font-weight: 300;
  font-size: 2.7em;
  color: #526488;
  word-spacing: 0.1em;
  padding-bottom: 0.4em;
  margin-bottom: 1em;
}
.recipe-title {
  font-weight: 300;
  font-size: 1.5em;
  color: #35495e;
  padding: 0.2em;
}
.reload {
  font-family: "Trebuchet MS", "Lucida Sans Unicode", "Lucida Grande",
    "Lucida Sans", Arial, sans-serif;
  font-size: 2em;
  color: whitesmoke;
}
.reload-btn {
  margin: 3em;
  border: none;
  border-radius: 2em;
  height: 4em;
  width: 4em;
  background: #35495e;
}
.reload-btn:hover {
  background: whitesmoke;
  border: 0.01em solid #35495e;
}
.reload-btn:hover > * {
  color: #35495e;
}
table {
  margin: auto;
  margin-top: 1.3em;
  margin-bottom: 2.3em;
  border-collapse: collapse;
  font-weight: 300;
  font-size: 1.1em;
  width: 77%;
}
td {
  padding-bottom: 0.4em;
  padding-top: 0.4em;
}
.td-left {
  text-align: right;
  padding-right: 1em;
  width: 33%;
  border-top-left-radius: 0.3em;
  border-bottom-left-radius: 0.3em;
}
.td-right {
  text-align: left;
  padding-left: 1em;
  border-top-right-radius: 0.3em;
  border-bottom-right-radius: 0.3em;
}
tr:nth-child(odd) {
  background-color: #f2f2f2;
}
p {
  font-size: 1.1em;
  padding-top: 0.5em;
}
.description {
  width: 77%;
  text-align: left;
  margin-left: auto;
  margin-right: auto;
}
</style>
