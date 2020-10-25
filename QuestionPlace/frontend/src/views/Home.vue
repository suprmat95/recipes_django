<template lang="html">
  <div class="home-view">
    <div class="container">
      <div class="row">
        <div v-for="question in questions" :key="question.pk">
          <!--  <p class="mb-0"> Domanda aggiunta da
                                                          <span class="author-name">{{ question.author }}</span>
                                                      </p>
                                  
                                                      <p>Risposte: {{question.answers_count}}</p> -->
          <div class="col-sm col-md">
            <router-link
                                :to="{ name: 'question', params: {slug: question.slug}}"
                                class="question-link">
            <md-card>
              <md-card-media>
                <img :src="question.picture" alt="People" />
              </md-card-media>

              <md-card-header>
                <div class="md-title">{{ question.content }}</div>
                <div class="md-subhead">
                  <p class="mb-0">
                    Ricetta aggiunta da
                    <span class="author-name">{{ question.author }}</span>
                  </p>
                  <p>Risposte: {{ question.answers_count }}</p>
                </div>
              </md-card-header>

              <md-card-expand>
                <md-card-actions md-alignment="space-between">
                  <div>
                    <md-button>Action</md-button>
                    <md-button>Action</md-button>
                  </div>

                  <md-card-expand-trigger>
                    <md-button class="md-icon-button">
                      <md-icon>keyboard_arrow_down</md-icon>
                    </md-button>
                  </md-card-expand-trigger>
                </md-card-actions>

                <md-card-expand-content>
                  <md-card-content>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Optio itaque ea, nostrum odio. Dolores, sed accusantium
                    quasi non, voluptas eius illo quas, saepe voluptate pariatur
                    in deleniti minus sint. Excepturi.
                  </md-card-content>
                </md-card-expand-content>
              </md-card-expand>
            </md-card>
            </router-link>
          </div>
        </div>
      </div>
      <div class="mt-4">
        <p v-show="loadingQuestions">...loading...</p>
        <button
          v-show="next"
          @click="getQuestions"
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
      questions: [],
      next: null,
      loadingQuestions: false
    };
  },
  methods: {
    getQuestions() {
      let endpoint = "api/questions/";
      if (this.next) {
        endpoint = this.next;
      }
      this.loadingQuestions = true;
      apiService(endpoint).then(data => {
        console.log(data.results);
        this.questions.push(...data.results);
        this.loadingQuestions = false;
        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    }
  },

  created() {
    document.title = "QuestionPlace";
    this.getQuestions();
  }
};
</script>
<style>
.author-name {
  font-weight: bold;
  color: #dc3545;
}

.question-link {
  font-weight: bold;
  color: black;
}

.question-link:hover {
  color: #343a40;
  text-decoration: none;
}

.home-view {
  text-align: left;
}

.md-card {
  width: 320px;
  margin: 4px;
  display: inline-block;
  vertical-align: top;
}
</style>
