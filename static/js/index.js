async function getArticles() {
  const response = await fetch("/articles/?skip=0&limit=10").then(res => res.json());
  return response;
}


async function getComments() {
  const response = await fetch("/comments/?skip=0&limit=10").then(res => res.json());
  return response;
}


async function getCommentsByArticleId(id) {
  const response = await fetch("/comments/?skip=0&limit=10").then(res => res.json());
  result = [];
  for (let comment of response) {
    if (comment["article_id"] == id) {
      result.push(comment);
    }
  }
  return result;
}


async function createArticle(name, content) {
  const response = await fetch('http://127.0.0.1:8000/articles/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify({
      name: name,
      content: content,

    })
  }).then(res => res.json());
  setArticle(response)
}


async function createComment(content, article_id) {
  const response = await fetch('http://127.0.0.1:8000/comments/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify({
      content: content,
      article_id: article_id
    })
  }).then(res => res.json());
}





// Создание статьи
const createArticleTemplate = (article, comments) => {
  commetnsTeamplate = '';
  for (let comment of comments) {
    if (comment["article_id"] == article["id"]) {
      commetnsTeamplate += `<p class="comments__comment">${comment["content"]}</p>`;
    }
  }

  const result = document.createElement('div');
  result.className = "main__articles-article article";
  result.innerHTML = `
    <div class="article__title">${article["name"]}</div>
    <p class="article__text">${article["content"]}</p>

    <div class="article__comments comments">
      <p class="comments__title">Комментарии</p>
      <div class="comments__list">
        ${commetnsTeamplate}
      </div>
    </div>
    <form class="article__add-comment"></form>`

  const button = document.createElement('button');
  const input = document.createElement('input');
  input.className = "article__input";
  input.placeholder = "ваш комментарий...";
  input.type = "text";
  button.className = "article__button button";
  button.innerHTML = "отправить";
  const article_id = article["id"]
  button.addEventListener("click", async () => {
    await createComment(input.value, article_id)
    console.log(input.value, article_id);
    result.querySelector(".comments__list").innerHTML += `<p class="comments__comment">${input.value}</p>`;
    input.value = '';
  });

  result.querySelector('.article__add-comment').append(input);
  result.querySelector('.article__add-comment').append(button);
  return result;
};




const setArticle = async (article) => {
  comments = await getCommentsByArticleId(article["id"])
  articleList.append(createArticleTemplate(article, comments));

}; 


const articleList = document.querySelector('.main__articles');
const loadArticle = document.querySelector('.main__load-article');
const chat = document.querySelector('.chat');

const articlesLink = document.querySelector('.navigation__link');
const createArticlesLink = document.querySelector('.navigation__link:nth-child(2)');
const chatLink = document.querySelector('.navigation__link:last-child');

const loadArticleButton = document.querySelector('.load-article__button');
const loadInput = document.querySelector('.load-article__input');
const loadTextarea = document.querySelector('.load-article__textarea');


articlesLink.addEventListener("click", () => {
  articleList.classList.remove("hidden");
  loadArticle.classList.add("hidden");
  chat.classList.add("hidden");
  articlesLink.classList.add("active");
  createArticlesLink.classList.remove("active");
  chatLink.classList.remove("active");
})

createArticlesLink.addEventListener("click", () => {
  articleList.classList.add("hidden");
  loadArticle.classList.remove("hidden");
  chat.classList.add("hidden");
  articlesLink.classList.remove("active");
  createArticlesLink.classList.add("active");
  chatLink.classList.remove("active");
})

chatLink.addEventListener("click", () => {
  articleList.classList.add("hidden");
  loadArticle.classList.add("hidden");
  chat.classList.remove("hidden");
  articlesLink.classList.remove("active");
  createArticlesLink.classList.remove("active");
  chatLink.classList.add("active");
})



loadArticleButton.addEventListener("click", async () => {
  await createArticle(loadInput.value, loadTextarea.value);
  console.log(loadInput.value, loadTextarea.value);
  loadInput.value = '';
  loadTextarea.value = '';
})


async function main() {
  const articles = await getArticles();
  const comments = await getComments();

  for (let article of articles) {
    setArticle(article, comments);
  }

}


main();