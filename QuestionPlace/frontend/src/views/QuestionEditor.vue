<template lang="html">
  <div class="container">
    <br />
    <h1 class="mb-3">Aggiungi una Ricetta</h1>
    <h3 class="mb-3 align-left">Aggiungi il titolo</h3>

    <div class="row">
      <div class="col-12">
        <!--   <form action="http://localhost:8000/api/questions/"
                                                                                          method="post"
                                                                                          encType="multipart/form-data"
                                                                                        > -->

        <md-field>
          <label>Titolo Ricetta</label>
          <md-input v-model="questionBody"></md-input>
        </md-field>
        <!--<textarea
                                          name="content"
                                          v-model="questionBody"
                                          class="form-control"
                                          placeholder="Aggiungi titolo alla ricetta?"
                                          rows="1"
                                        ></textarea>-->
        <br />
      </div>
    </div>
    <br />
    <hr />
    <h3 class="mb-3 align-left">Aggiungi foto</h3>
    <div class="row">
      <div class="col-12">
        <picture-input
          @change="onChange($event)"
          class="align-left"
          name="picture"
          ref="file"
          width="200"
          height="200"
          margin="16"
          accept="image/jpeg,image/png, image/png"
          size="5"
          buttonClass="btn"
          :customStrings="{
            upload: '<h1>RECIPEEE!</h1>',
            drag: 'Drag a 😺 GIF'
          }"
        >
        </picture-input>
      </div>
    </div>
    <br />
    <br />
    <hr />

    <h3 class="mb-3 align-left">Aggiungi Ingredienti</h3>
    <md-button
      class="md-icon-button md-raised align-left"
      @click="addRowIngredient"
    >
      <md-icon>add</md-icon>
    </md-button>
    <li v-for="(ingredient, index) in ingredients" :key="index">
      <div class="row">
        <div class="col-12">
          <md-field class="form-control-ing-name">
            <label>Nome ingrediente</label>
            <md-input v-model="ingredient.name"></md-input>
          </md-field>
          <md-field class="form-control-ing-quantity">
            <label>Quantità</label>
            <md-input v-model="ingredient.quantity"></md-input>
          </md-field>

          <md-field class="md-layout-item">
            <label>Unità</label>
            <md-select v-model="ingredient.unity" name="unity" id="unity">
              <md-option value="grams">Grams</md-option>
              <md-option value="liter">Liter</md-option>
            </md-select>
          </md-field>
          <br />
          <md-button
            class="md-icon-button md-raised align-left child"
            @click="deleteRowIngredient(index)"
          >
            <md-icon> delete</md-icon>
          </md-button>
        </div>
      </div>
    </li>
    <br />
    <hr />
    <h3 class="mb-3 align-left">Aggiungi Passaggi</h3>
    <md-button
      class="md-icon-button md-raised align-left"
      @click="addRowPassage"
    >
      <md-icon>add</md-icon>
    </md-button>

    <li v-for="(input, index) in inputs" :key="'A'+index">
      <div class="row">
        <div class="col-12">
          <!--   <form action="http://localhost:8000/api/questions/" -->
          <md-field class="form-passage">
            <label>Spiegazione del passaggio</label>
            <md-input v-model="input.body"></md-input>
          </md-field>
          <md-button
            class="md-icon-button md-raised "
            @click="deleteRowPassage(index)"
          >
            <md-icon> delete</md-icon>
          </md-button>
        </div>
      </div>

      <br />
      <div class="hello">
        <picture-input
          @change="handleFileChange($event, index)"
          class="align-left"
          name="picture"
          ref="file"
          width="150"
          height="150"
          margin="16"
          accept="image/jpeg,image/png,image/gif"
          size="5"
          buttonClass="btn"
          :customStrings="{
            upload: '<h1>RECIPEEE!</h1>',
            drag: 'Drag a 😺 GIF'
          }"
        >
        </picture-input>
      </div>
    </li>

    <br />
    <br />
    <div class="row">
      <div class="col-12">
        <md-button class="md-raised md-primary align-left" @click="onSubmit">
          UPLOAD
        </md-button>
      </div>
    </div>

    <p class="muted error mt-2">{{ error }}</p>
  </div>
</template>

<script>
import { apiService } from "../common/api.service";
import PictureInput from "vue-picture-input";
import { CSRF_TOKEN } from "../common/csrf_token.js";
import axios from "axios";

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
      movie: "good father",
      inputs: [],
      ingredients: [],

      questionBody: this.previousQuestion || null,
      error: null,
      picture: null
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
    dataURLtoFile(dataurl, filename) {
      var arr = dataurl.split(","),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);

      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }

      return new File([u8arr], filename, { type: mime });
    },
    addRowPassage() {
      this.inputs.push({
        body: "",
        picture: null
      });
    },
    addRowIngredient() {
      this.ingredients.push({
        name: "",
        quantity: null,
        unity: ""
      });
    },
    deleteRowPassage(index) {
      this.inputs.splice(index, 1);
    },
    deleteRowIngredient(index) {
      this.ingredients.splice(index, 1);
    },
    handleFileChange(event, index) {
      console.log("New picture selected!");
      if (event) {
        console.log("Squalo");
        // document.getElementById("token").setAttribute("value", this.token);
        //  console.log(document.getElementById("token").getAttribute("value"));

        console.log("Picture loaded.");
        this.inputs[index].picture = this.dataURLtoFile(
          event,
          this.questionBody + "-picture.jpg"
        );
        console.log(this.inputs[index].picture);
      } else {
        console.log("FileReader API not supported: use the <form>, Luke!");
      }
    },
    onChange(event) {
      console.log("New picture selected!");
      if (event) {
        console.log("Squalo");
        // document.getElementById("token").setAttribute("value", this.token);
        //  console.log(document.getElementById("token").getAttribute("value"));

        console.log("Picture loaded.");
        this.picture = this.dataURLtoFile(
          event,
          this.questionBody + "-picture.jpg"
        );
        console.log(this.picture);
      } else {
        console.log("FileReader API not supported: use the <form>, Luke!");
      }
    },
    onSubmit() {
      const headers = { "X-CSRFTOKEN": CSRF_TOKEN };
      const fd = new FormData();

      fd.append("content", this.questionBody);
      fd.append("picture", this.picture, this.picture.name);
      console.log(fd);
      console.log("body " + this.questionBody);
      console.log(this.picture);
      console.log("picname " + this.picture.name);

      const endpoint = "http://localhost:8000/api/questions/";
      axios
        .post(endpoint, fd, { headers: headers })
        .then(question_data => {
          console.log(question_data.data.slug);
          this.inputs.forEach(input => {
            const fp = new FormData();
            fp.append("body", input.body);
            fp.append("picture", input.picture);
            axios
              .post(endpoint + question_data.data.slug + "/passage/", fp, {
                headers: headers
              })
              .then(res => {
                console.log("recipes res");
                console.log(res);
              });
          });
          this.ingredients.forEach(ingredient => {
            const fi = new FormData();
            console.log("Prova:");
            console.log(ingredient.name);
            console.log(ingredient.quantity);
            console.log(ingredient.unity);
            fi.append("name", ingredient.name);
            fi.append("quantity",ingredient.quantity)
            fi.append("unity",ingredient.unity)
            axios
              .post(endpoint + question_data.data.slug + "/ingredient/", fi, {
                headers: headers
              })
              .then(res => {
                console.log("recipes ingredients");
                console.log(res);
              });

          });
        })
        .catch(err => console.log(err));
    }

    // onSubmit() {
    //   if (!this.questionBody) {
    //     this.error = "Il campo non puo essere vuoto.";
    //   } else if (this.questionBody.length > 240) {
    //     this.error = "Non superare i 240 caratteri.";
    //   } else {
    //     let endpoint = "/api/questions/";
    //     let method = "POST";
    //     if (this.previousQuestion) {
    //       method = "PUT";
    //       endpoint += `${this.slug}/`;
    //     }
    //     apiService(endpoint, method, {content: this.questionBody}).then(
    //       question_data => {
    //         this.$router.push({
    //           name: "question",
    //           params: { slug: question_data.slug }
    //         });
    //       }
    //     );
    //   }
    // }
  },
  created() {
    document.title = "Editor - QuestionPlace";
    console.log("created");
    this.inputs.push({
      body: "",
      image: null
    });
    this.ingredients.push({
      name: "",
      quantity: "",
      unity: ""
    });
  }
};
</script>

<style scoped>
.form-control {
  width: 60%;
  float: left;
}

.row {
  width: 100%;
}

.align-right {
  float: right;
}

.hello {
  width: 50%;
  float: left;
}

.align-left {
  float: left;
  margin: 10px;
}

.form-control-ing-name {
  float: left;
  width: 30%;
  margin: 10px;
  height: 45px;
}

.form-control-ing-quantity {
  float: left;
  width: 15%;
  height: 45px;
  margin: 10px;
}

.md-layout-item {
  float: left;
  width: 10%;
  margin: 10px;
}

.form-passage {
  float: left;
  width: 80%;
}
</style>
