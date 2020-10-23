<template lang="html">
  <div class="container mt-2">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-3">Aggiungi una domanda</h1>
        <form action='http://localhost:8000/api/questions/'  method='post'
            encType="multipart/form-data">
          <textarea
                  name ="content"
            v-model="questionBody"
            class="form-control"
            placeholder="Cosa vuoi chiedere?"
            rows="3"
          ></textarea>
            <div class="hello">
            <picture-input
                    name="picture"
              ref="picture"
              @change="onChange"
              width="600"
              height="600"
              margin="16"
              accept="image/jpeg,image/png"
              size="10"
              buttonClass="btn"
              :customStrings="{
                upload: '<h1>Bummer!</h1>',
                drag: 'Drag a 😺 GIF or GTFO'
              }">
        </picture-input>

            </div>
          <br />
          <input id="token" type="hidden" name="csrfmiddlewaretoken"  />

          <input type='submit' value='Upload!' />

        </form>
        <p class="muted error mt-2">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
import PictureInput from "vue-picture-input";
import { CSRF_TOKEN } from "../common/csrf_token.js";

export default {
  name: "QuestionEditor",
    components: {
    PictureInput
  },
  props: {
    slug: {
      type: String,
      error: null
    },
    previousQuestion: {
      type: String,
      required: false
    },
    token: {
     type: String,
     required: true
    }
  },
  data() {
    return {
      questionBody: this.previousQuestion || null,
      error: null,
      picture: null,
    };
  },

  async beforeRouteEnter(to, from, next) {
    to.params.token = CSRF_TOKEN;

    console.log(to.params.token);

    if (to.params.slug !== undefined) {
      let endpoint = `/api/questions/${to.params.slug}/`;
      await apiService(endpoint).then(data => {
        to.params.previousQuestion = data.content;
      });
    }
    return next();
  },
  methods: {
    onChange(image) {
      console.log("New picture selected!");
      if (image) {
        console.log("Squalo");
        document.getElementById("token").setAttribute("value", this.token);
        console.log(document.getElementById("token").getAttribute("value"));

        console.log("Picture loaded.");
        this.picture = image;
        console.log(this.picture);
      } else {
        console.log("FileReader API not supported: use the <form>, Luke!");
      }
    },
    onSubmit() {
      if (!this.questionBody) {
        this.error = "Il campo non puo essere vuoto.";
      } else if (this.questionBody.length > 240) {
        this.error = "Non superare i 240 caratteri.";
      } else {
        let endpoint = "/api/questions/";
        let method = "POST";
        if (this.previousQuestion) {
          method = "PUT";
          endpoint += `${this.slug}/`;
        }
        apiService(endpoint, method, {content: this.questionBody}).then(
          question_data => {
            this.$router.push({
              name: "question",
              params: { slug: question_data.slug }
            });
          }
        );
      }
    }
  },
  created() {
    document.title = "Editor - QuestionPlace";
        console.log("created")

  }
};
</script>

<style scoped></style>
