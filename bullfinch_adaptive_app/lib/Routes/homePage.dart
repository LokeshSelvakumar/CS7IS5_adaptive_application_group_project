import 'dart:html';

import 'package:flutter/material.dart';
import '../widgets/news.dart';
import '../widgets/stocks.dart';
import '../widgets/recommendedStocks.dart';
import '../models/news_model.dart';
import '../models/stocks_model.dart';

/*
* UI for showing news and stocks
*
* */
class HomePage extends StatefulWidget {
    createState(){
        return HomePageState();
    }
}

class HomePageState extends State<HomePage>{
  MySearchBarState searchBar = MySearchBarState();
  Widget build(context){
      return MaterialApp(
          home: Scaffold(
              appBar: AppBar(
                  title: Text('Your Feed'),
              ),
              body: Wrap(
                  spacing: 20,
                  children: <Widget>[
                      //MySearchBar(),
                      Container(
                          height: 500,
                          width: 500,
                          margin: EdgeInsets.only(left: 100, top: 20, bottom: 20),
                          padding: EdgeInsets.all(20),
                          decoration: BoxDecoration(
                              color: Colors.teal.shade100,
                              borderRadius: BorderRadius.circular(10),
                          ),
                          child: News([])
                      ),
                      Container(
                          height: 500,
                          width: 500,
                          margin: EdgeInsets.all(20),
                          padding: EdgeInsets.all(20),
                            decoration: BoxDecoration(
                              color: Colors.teal.shade100,
                              borderRadius: BorderRadius.circular(10),
                          ),
                          child: Column(
                            children: [
                              ElevatedButton.icon(
                                onPressed: () {
                                  print("search");
                                  searchBar.showSearch();
                                }, 
                                icon: Icon(
                                  Icons.search
                                ), 
                                label: Text("Search Stocks"),
                              ),
                              Container(
                                height: 250,
                                width: 500,
                                
                                decoration: BoxDecoration(
                                  //color: Colors.teal,
                                  borderRadius: BorderRadius.circular(5),
                                ),
                                child: Stocks([]),
                              ),//Stock
                              Container(
                                height: 150,
                                width: 500,
                                margin: EdgeInsets.only(top: 30),
                                padding: EdgeInsets.all(5),
                                decoration: BoxDecoration(
                                  color: Colors.cyan.shade700,
                                  borderRadius: BorderRadius.circular(5),
                                ),
                                child: Column(
                                  children: [
                                    Text("Recommended Stocks"),
                                    RecommendedStocks([])
                                  ],
                                )
                              )//recommended stock
                            ],
                          )
                      ),
                  ]
              )
          )
      );
  }
}

class MySearchBar extends StatefulWidget{
  @override
  MySearchBarState createState() => MySearchBarState();
}

class MySearchBarState extends State<MySearchBar>{
  bool isOnScreen = false;

  void showSearch(){
    setState((){
      isOnScreen = true;
    });
  }

  void hideSearch(){
    setState((){
      isOnScreen = true;
    });
  }

  Widget build(BuildContext context){
    return Visibility(
      maintainAnimation: true,
      maintainSize: true,
      maintainState: true,
      visible: isOnScreen,
      child: Container(
        width: 600,
        height: 500,
        color: Colors.red.shade300,
        child: Text("Search Bar"),
        padding: EdgeInsets.all(20),
      )
    );
  }
}