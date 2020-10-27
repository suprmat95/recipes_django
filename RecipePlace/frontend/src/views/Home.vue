<template lang="html">
  <div class="home-view">
    <div class="container">
      <br />
      <div class="row">
        <div v-for="recipe in recipes" :key="recipe.pk">
          <div class="col-sm col-md">
            <router-link
              :to="{ name: 'recipe', params: { slug: recipe.slug } }"
              class="recipe-link"
            >
              <md-card >
                <md-card-media>
                    <img :src="recipe.picture" alt="People" style="height:210px;"/>
                </md-card-media>

                <md-card-header>
                  <div class="md-title">{{ recipe.content }}</div>
                  <div class="md-subhead">
                    <p class="mb-0">
                      Ricetta aggiunta da
                      <span class="author-name">{{ recipe.author }}</span>
                    </p>
                    <p>Commenti: {{ recipe.comments_count }}</p>
                  </div>
                </md-card-header>

                <md-card-expand>
                  <md-card-actions  md-alignment="space-between">
                    <div>
                      <md-button class="button btn btn-sm ">
                        <md-icon>favorites</md-icon>
                      </md-button>
                      <md-button class="button btn btn-sm ">
                        <md-icon>share</md-icon>
                      </md-button>
                      <md-button class="button btn btn-sm ">
                        <md-icon>bookmark_border</md-icon>
                      </md-button>
                    </div>
                  </md-card-actions>
                </md-card-expand>
              </md-card>
            </router-link>
          </div>
        </div>
      </div>
      <div class="mt-4">
        <p v-show="loadingRecipes">...loading...</p>
        <button
          v-show="next"
          @click="getRecipes"
          class="btn btn-sm btn-outline-success"
        >
          Carica Ancora
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";

export default {
  name: "Home",

  data() {
    return {
      recipes: [],
      next: null,
      loadingRecipes: false
    };
  },
  methods: {
    getRecipes() {
      let endpoint = "/api/recipes/";
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingRecipes = true;
      apiService(endpoint)
        .then(data => {
          this.recipes.push(...data.results);
          this.loadingRecipes = false;
          if (data.next) {
            this.next = data.next;
          } else {
            this.next = null;
          }
        })
        .catch(e => {
          console.log("Errror:");
          console.log(e);
        });
    }
  },

  created() {
    document.title = "RecipePlace";
    this.getRecipes();
  }
};
</script>
<style>
.author-name {
  font-weight: bold;
  color: #dc3545;
}

.recipe-link {
  font-weight: bold;
  color: black;
}

.recipe-link:hover {
  color: #343a40;
  text-decoration: none;
}

.home-view {
  text-align: left;
}

.md-card {
  width: 320px;
  margin: 4px;
  height: 400px;
  display: inline-block;
  vertical-align: top;
  border-radius: 15px;
  margin-bottom: 15px;
}
</style>
