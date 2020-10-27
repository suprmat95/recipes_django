<template lang="html">
  <div class="single-recipe mt-2">
    <div v-if="notFound" class="container">
      <h1>Ricetta non trovata!</h1>
    </div>
    <div v-else class="container">
      <div class="container">
        <div align="right">
          <RecipeActions v-if="isOwner" :slug="slug" />
        </div>
        <br />
        <br />
        <div align="center">
          <img align="center" id="picture" width="500" height="500" />
        </div>
        <br />
        <h1>{{ recipe.content }}</h1>
        <h5>{{ recipe.description }}</h5>
        <br />
        <hr />
        <h3><md-icon>av_timer</md-icon> {{ recipe.time_to_prepare }} minuti </h3>
        <br />
        <h3><md-icon>people</md-icon> {{ recipe.people }} persone</h3>
        <hr />

        <h2 class="mb-3 align-left">Ingredienti</h2>
        <div class="row">
          <div class="col-sm">
            <ul>
              <li v-for="(ingredient, index) in ingredients" :key="index">
                <h5>
                  {{ ingredient.name }} {{ ingredient.quantity }}
                  {{ ingredient.unity }}
                </h5>
              </li>
            </ul>
          </div>
        </div>
        <br />
        <hr />
        <h2 class="mb-3 align-left">Passaggi</h2>
        <div class="row">
          <div v-for="(passage, index) in passages.reverse()" :key="'A' + index">
            <div class="col-sm col-md">
              <md-card class="card">
                <md-card-media>
                  <img :src="passage.picture" alt="People" style="height:220px;" />
                </md-card-media>
                <div class="md-title">
                  <p align="center" style="margin-top: 7px">Passaggio {{ index + 1 }}</p>
                  <hr />
                </div>

                <md-card-content>
                  <b>{{ passage.body }}</b>
                </md-card-content>
              </md-card>
            </div>
            <br />
            <br />
          </div>
        </div>

        <p class="mb-0">
          Ricetta aggiunta da:
          <span class="author-name">{{ recipe.author }}</span>
        </p>
        <p>{{ recipe.created_at }}</p>
        <hr />
        <template v-if="userHasCommented">
          <p class="comment-added">Hai commentanto questa ricetta.</p>
        </template>
        <template v-else-if="showForm">
          <form class="card" @submit.prevent="onSubmit">
            <div class="card-header px-3">
              Aggiungi un commento alla ricetta
            </div>
            <div class="card-block">
              <textarea
                v-model="newCommentBody"
                class="form-control"
                placeholder="Aggiungi un commento alla ricetta"
                rows="10"
              ></textarea>
            </div>
            <div class="card-footer px-3">
              <button type="submit" class="btn btn-sm btn-success">
                Aggiungi Commento
              </button>
            </div>
          </form>
          <p class="error mt-2">{{ this.error }}</p>
        </template>
        <template v-else>
          <button class="btn btn-sm btn-success" @click="showForm = true">
            Commenta la ricetta
          </button>
        </template>
        <hr />
        <CommentComponent
          v-for="(comment, index) in comments"
          :comment="comment"
          :requestUser="requestUser"
          :key="index"
          @delete-comment="deleteComment"
        />
        <div class="my-4">
          <p v-show="loadingComments">...loading...</p>
          <button
            v-show="next"
            @click="getRecipeComments"
            class="btn btn-sm btn-outline-succes"
          >
            Carica Ancora
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
import CommentComponent from "../components/Comment";
import RecipeActions from "../components/RecipeActions";

export default {
  name: "Recipe",

  props: {
    slug: {
      type: String,
      required: true
    }
  },
  components: {
    RecipeActions,
    CommentComponent
  },
  data() {
    return {
      recipe: {},
      loadingComments: false,
      comments: [],
      ingredients: [],
      passages: [],
      userHasCommented: false,
      showForm: false,
      newCommentBody: null,
      error: null,
      next: null,
      requestUser: null
    };
  },
  computed: {
    isOwner() {
      return this.recipe.author === this.requestUser;
    },
    notFound() {
      return this.recipe["detail"];
    }
  },
  methods: {
    setPageTitle(title) {
      document.title = title;
    },
    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    },
    getRecipeData() {
      let endpoint = `/api/recipes/${this.slug}/`;
      apiService(endpoint).then(data => {
        this.recipe = data;
        this.ingredients = this.recipe.ingredient;
        this.passages = this.recipe.passage;
        document
          .getElementById("picture")
          .setAttribute("src", this.recipe.picture);

        this.userHasCommented = data.user_has_commented;
        this.setPageTitle(data.content);
      });
    },
    getRecipeComments() {
      let endpoint = `/api/recipes/${this.slug}/comments/`;
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingComments = true;
      apiService(endpoint).then(data => {
        this.comments.push(...data.results);
        this.loadingComments = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },
    onSubmit() {
      if (this.newCommentBody) {
        let endpoint = `/api/recipes/${this.slug}/comment/`;

        apiService(endpoint, "POST", { body: this.newCommentBody }).then(
          data => {
            this.comments.unshift(data);
          }
        );

        this.newCommentBody = null;
        this.showForm = false;
        this.userHasCommented = true;
        if (this.error) {
          this.error = null;
        }
      } else {
        this.error = "Il campo non puo essere vuoto.";
      }
    },
    async deleteComment(comment) {
      let endpoint = `/api/comment/${comment.id}/`;
      try {
        await apiService(endpoint, "DELETE");
        this.$delete(this.comments, this.comments.indexOf(comment));
        this.userHasCommented = false;
      } catch (err) {
        console.log(err);
      }
    }
  },
  created() {
    this.getRecipeData();
    this.getRecipeComments();
    this.setRequestUser();
  }
};
</script>

<style scoped>
.single-recipe {
  text-align: left;
}

.error {
  color: red;
  font-weight: bold;
}

.comment-added {
  color: green;
  font-weight: bold;
}

.card {
  height: 350px;
  border-radius: 20px;
}
</style>
