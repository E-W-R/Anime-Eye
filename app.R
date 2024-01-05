
library(shiny)
library(reticulate)

ui <- fluidPage(
    tags$style(HTML("
    body {
      background-color: #e8dbcc;
      padding: 10px;
      text-align: center;
    }
    .shiny-html-output {
      margin-bottom: 10px;
    }
  ")),
  fluidRow(
    column(3, # style = "background-color: white; border: 4px solid black;",
      h3("Safe Picks"),
      hr(style = "border-top: 4px solid #000000;"),
      fluidRow(
        column(6, align = "center", htmlOutput("pick1")),
        column(6, align = "center", htmlOutput("pick2")),
      ),
      fluidRow(
        column(6, align = "center", htmlOutput("pick3")),
        column(6, align = "center", htmlOutput("pick4")),
      ),
      fluidRow(
        column(6, align = "center", htmlOutput("pick5")),
        column(6, align = "center", htmlOutput("pick6")),
      ),
      fluidRow(
        column(6, align = "center", htmlOutput("pick7")),
        column(6, align = "center", htmlOutput("pick8")),
      ),
    ),
    
    column(6, style = "padding: 20px",
      imageOutput("eye"),
      
      fluidRow(
        column(4, textInput("user", "Username", placeholder = "ex. Evan0", width = "100%")),
        column(8, selectInput("model", "Model", c("User-based collaborative filtering", "Item-based collaborative filtering"), width = "100%"))
      ),
      actionButton("go", "Generate", width = "100%"),
      
      hr(style = "border-top: 2px solid #000000;"),
      textOutput("roast")
    ),
    
    column(3, # style = "background-color: white; border: 4px solid black;",
      h3("Wild Cards"),
      hr(style = "border-top: 4px solid #000000;"),
      fluidRow(
        column(6, align = "center", htmlOutput("pick11")),
        column(6, align = "center", htmlOutput("pick12")),
      ),
      fluidRow(
        column(6, align = "center", htmlOutput("pick13")),
        column(6, align = "center", htmlOutput("pick14")),
      ),
      fluidRow(
        column(6, align = "center", htmlOutput("pick15")),
        column(6, align = "center", htmlOutput("pick16")),
      ),
      fluidRow(
        column(6, align = "center", htmlOutput("pick17")),
        column(6, align = "center", htmlOutput("pick18")),
      ),
    ),
  )
)

server <- function(input, output) {
  dir <- getwd()
  my_url <- "https://i.ibb.co/K7jCBTP/placeholder-2.png"
  output$eye <- renderImage(list(src = paste0(dir, "/images/Anime Eye.gif"), contentType = "image/png", width = "100%", height = "100%"), deleteFile = FALSE)
  output$pick1 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick2 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick3 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick4 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick5 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick6 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick7 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick8 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick11 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick12 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick13 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick14 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick15 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick16 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick17 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))
  output$pick18 <- renderUI(tags$img(src = my_url, width = "100%", height = "auto"))

  output$roast <- renderText("Hello, and welcome to the Anime Eye.
                             The app uses various recommendation algorithms to intelligently recommend anime for you based on what you’ve enjoyed so far. All you need to do is give your MyAnimeList username and press “Generate”.")
  
  last_user <- ""
  load("app.RData")
  reticulate::source_python("main.py")
  
  observeEvent(input$go, {
    vec <- vector(input$user, df)
    if (input$model == "User-based collaborative filtering") {
      out <- user_cf(vec, df)
    } else{
      out <- item_cf(vec, df)
    }
    output$pick1 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][1]), target = "_blank", tags$img(src = out[[1]][1], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick2 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][2]), target = "_blank", tags$img(src = out[[1]][2], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick3 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][3]), target = "_blank", tags$img(src = out[[1]][3], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick4 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][4]), target = "_blank", tags$img(src = out[[1]][4], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick5 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][5]), target = "_blank", tags$img(src = out[[1]][5], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick6 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][6]), target = "_blank", tags$img(src = out[[1]][6], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick7 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][7]), target = "_blank", tags$img(src = out[[1]][7], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick8 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[3]][8]), target = "_blank", tags$img(src = out[[1]][8], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    
    output$pick11 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][1]), target = "_blank", tags$img(src = out[[2]][1], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick12 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][2]), target = "_blank", tags$img(src = out[[2]][2], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick13 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][3]), target = "_blank", tags$img(src = out[[2]][3], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick14 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][4]), target = "_blank", tags$img(src = out[[2]][4], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick15 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][5]), target = "_blank", tags$img(src = out[[2]][5], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick16 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][6]), target = "_blank", tags$img(src = out[[2]][6], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick17 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][7]), target = "_blank", tags$img(src = out[[2]][7], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    output$pick18 <- renderUI(tags$a(href = paste0("https://myanimelist.net/anime/", out[[4]][8]), target = "_blank", tags$img(src = out[[2]][8], width = "100%", height = "auto", style = "border: 4px solid #000;")))
    
    if (last_user != input$user) {
      output$roast <- renderText(message(vec, df))
      last_user <<- input$user
    }
  })
}

shinyApp(ui = ui, server = server)
