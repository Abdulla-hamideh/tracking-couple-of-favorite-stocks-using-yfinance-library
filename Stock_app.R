library(shinydashboard)
library(shiny)

ui<- shinyUI(
  dashboardPage( 
    dashboardHeader(title= "Retail Predictive Model", titleWidth = 250),
    dashboardSidebar(
      menuItem("Sales Dashboard")
    ),
    dashboardBody(
      fluidRow(
        box(
          title = "Enter Stock Code", width = 4, solidHeader = TRUE, status = "primary",
          textInput("StockCode", "StockCode", value = "AAPL"),
          radioButtons("seasonal", "Select", c(NonSeasonal = "NonSeasonal", Seasonal = "Seasonal")),
          actionButton(inputId = "click", label = "Predict")
        )
      ),
      fluidRow(
        box(title = "Auto Arima - Non Seasonal",status = "primary",plotOutput("auto.arima", height = 350),height = 400),
        box(title = "Auto Arima - Non Seasonal",width = 6,tableOutput("auto.arima1"))
      ),
      fluidRow(
        box(title = "Auto Arima Seasonal",status = "primary",plotOutput("arima.seasonal", height = 350),height = 400),
        box(title = "Auto Arima Seasonal",width = 6,tableOutput("arima.seasonal1"))
      )
    )
  )
)


server <- function(input, output) {

  
  set.seed(122)
  histdata <- rnorm(500)

  output$plot1 <- renderPlot({
    if (is.null(input$count) || is.null(input$fill))
      return()

    data <- histdata[seq(1, input$count)]
    color <- input$fill
    if (color == "none")
      color <- NULL
    hist(data, col = color, main = NULL)
  })
  
  
#Auto.Arima - plot here  Tile#4 
  output$auto.arima <- renderPlot({
    
  
    # if (is.null(input$StockCode))
    #   return()
    library('quantmod')
    library('ggplot2')
    library('forecast')
    library('tseries')
    #Stock <- as.character(input$StockCode)
    
    data <- eventReactive(input$click, {
      (input$StockCode) 
    })
    Stock <- as.character(data())
    print(Stock)
    #getSymbols("AAPL", src = "yahoo",from="2017-07-01")
   # plot(AAPL$AAPL.Close)  
    Stock_df<-as.data.frame(getSymbols(Symbols = Stock, 
                                   src = "yahoo", from = "2016-01-01", env = NULL))
    Stock_df$Open = Stock_df[,1]
    Stock_df$High = Stock_df[,2]
    Stock_df$Low = Stock_df[,3]
    Stock_df$Close = Stock_df[,4]
    Stock_df$Volume = Stock_df[,5]
    Stock_df$Adj = Stock_df[,6]
    Stock_df <- Stock_df[,c(7,8,9,10,11,12)] 
    
    
    
    #plot(as.ts(Stock_df$Close))
    
    Stock_df$v7_MA = ma(Stock_df$Close, order=7)
    Stock_df$v30_MA <- ma(Stock_df$Close, order=30)
    
    #STL
    rental_ma <- ts(na.omit(Stock_df$v7_MA), frequency=30)
    decomp_rental <- stl(rental_ma, s.window="periodic")
    #plot(decomp_rental)
    adj_rental <- seasadj(decomp_rental)
    #plot(adj_rental)
    
    
    #arima
    fit <- auto.arima(Stock_df$Close,ic="bic")
    fit.forecast <- forecast(fit)
    plot(fit.forecast,  main= Stock)
   
 })

       #Auto.Arima1 - plot here  Tile#5
     output$auto.arima1 <- renderTable({
     #if (is.null(input$StockCode))
     #  return()
     library('quantmod')
     library('ggplot2')
     library('forecast')
     library('tseries')

     #Stock <- as.character(input$StockCode)
      data <- eventReactive(input$click, {
        (input$StockCode)
       })
      Stock <- as.character(data())
      print(Stock)
     #getSymbols("AAPL", src = "yahoo",from="2017-07-01")
     # plot(AAPL$AAPL.Close)
     Stock_df<-as.data.frame(getSymbols(Symbols = Stock,
                                        src = "yahoo", from = "2016-01-01", env = NULL))
     Stock_df$Open = Stock_df[,1]
     Stock_df$High = Stock_df[,2]
     Stock_df$Low = Stock_df[,3]
     Stock_df$Close = Stock_df[,4]
     Stock_df$Volume = Stock_df[,5]
     Stock_df$Adj = Stock_df[,6]
     Stock_df <- Stock_df[,c(7,8,9,10,11,12)]

     #plot(as.ts(Stock_df$Close))

     Stock_df$v7_MA = ma(Stock_df$Close, order=7)
     Stock_df$v30_MA <- ma(Stock_df$Close, order=30)

     #STL
     rental_ma <- ts(na.omit(Stock_df$v7_MA), frequency=30)
     decomp_rental <- stl(rental_ma, s.window="periodic")
     #plot(decomp_rental)
     adj_rental <- seasadj(decomp_rental)
     #plot(adj_rental)


     #arima
     fit <- auto.arima(Stock_df$Close,ic="bic")
     fit.forecast <- forecast(fit)
     #plot(fit.forecast,   col = "red")
     (fit.forecast)
   })
     
     #Auto.Arima Seasonal 
     output$arima.seasonal <- renderPlot({
       if (input$seasonal == "NonSeasonal")
         return()
       library('quantmod')
       library('ggplot2')
       library('forecast')
       library('tseries')
       
       #Stock <- as.character(input$StockCode)
       data <- eventReactive(input$click, {
         (input$StockCode)
       })
       Stock <- as.character(data())
       print(Stock)
       #getSymbols("AAPL", src = "yahoo",from="2017-07-01")
       # plot(AAPL$AAPL.Close)
       Stock_df<-as.data.frame(getSymbols(Symbols = Stock,
                                          src = "yahoo", from = "2016-01-01", env = NULL))
       Stock_df$Open = Stock_df[,1]
       Stock_df$High = Stock_df[,2]
       Stock_df$Low = Stock_df[,3]
       Stock_df$Close = Stock_df[,4]
       Stock_df$Volume = Stock_df[,5]
       Stock_df$Adj = Stock_df[,6]
       Stock_df <- Stock_df[,c(7,8,9,10,11,12)]
       
       #plot(as.ts(Stock_df$Close))
       
       Stock_df$v7_MA = ma(Stock_df$Close, order=7)
       Stock_df$v30_MA <- ma(Stock_df$Close, order=30)
       
       #STL
       rental_ma <- ts(na.omit(Stock_df$v7_MA), frequency=30)
       decomp_rental <- stl(rental_ma, s.window="periodic")
       #plot(decomp_rental)
       adj_rental <- seasadj(decomp_rental)
       #plot(adj_rental)
       
       
       #arima
       #fit <- auto.arima(Stock_df$Close,ic="bic")
       #fit.forecast <- forecast.Arima(fit)
       #plot(fit.forecast,   col = "red")
       #(fit.forecast)
       fit_s<-auto.arima(adj_rental, seasonal=TRUE)
       fcast_s <- forecast(fit_s, h=1000)
     })
     
     #Auto.Arima Seasonal 
     output$arima.seasonal1 <- renderTable({
       #if (is.null(input$StockCode))
       #  return()
       if (input$seasonal == "NonSeasonal")
         return()
       library('quantmod')
       library('ggplot2')
       library(forecast)
       library('tseries')
       
       #Stock <- as.character(input$StockCode)
       data <- eventReactive(input$click, {
         (input$StockCode)
       })
       Stock <- as.character(data())
       print(Stock)
       #getSymbols("AAPL", src = "yahoo",from="2017-07-01")
       # plot(AAPL$AAPL.Close)
       Stock_df<-as.data.frame(getSymbols(Symbols = Stock,
                                          src = "yahoo", from = "2016-01-01", env = NULL))
       Stock_df$Open = Stock_df[,1]
       Stock_df$High = Stock_df[,2]
       Stock_df$Low = Stock_df[,3]
       Stock_df$Close = Stock_df[,4]
       Stock_df$Volume = Stock_df[,5]
       Stock_df$Adj = Stock_df[,6]
       Stock_df <- Stock_df[,c(7,8,9,10,11,12)]
       
       #plot(as.ts(Stock_df$Close))
       
       Stock_df$v7_MA = ma(Stock_df$Close, order=7)
       Stock_df$v30_MA <- ma(Stock_df$Close, order=30)
       
       #STL
       rental_ma <- ts(na.omit(Stock_df$v7_MA), frequency=30)
       decomp_rental <- stl(rental_ma, s.window="periodic")
       #plot(decomp_rental)
       adj_rental <- seasadj(decomp_rental)
       #plot(adj_rental)
       
       
       #arima
       #fit <- auto.arima(Stock_df$Close,ic="bic")
       #fit.forecast <- forecast.Arima(fit)
       #plot(fit.forecast,   col = "red")
       #(fit.forecast)
      fit_s<-auto.arima(adj_rental, seasonal=TRUE)
      fcast_s <- forecast(fit_s, h=1000)
      fcast_s
     })
     
     
  output$scatter1 <- renderPlot({
    spread <- as.numeric(input$spread) / 100
    x <- rnorm(1000)
    y <- x + rnorm(1000) * spread
    plot(x, y, pch = ".", col = "blue")
  })

  output$scatter2 <- renderPlot({
    spread <- as.numeric(input$spread) / 100
    x <- rnorm(1000)
    y <- x + rnorm(1000) * spread
    plot(x, y, pch = ".", col = "red")
  })
  
  
}

shinyApp(ui, server)

