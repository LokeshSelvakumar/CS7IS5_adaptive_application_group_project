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
  //MySearchBarState searchBar = MySearchBarState();
  Widget build(context){
      return MaterialApp(
          home: Scaffold(
              appBar: AppBar(
                  title: Text('Your Feed'),
              ),
              body: Wrap(
                  spacing: 20,
                  children: <Widget>[
                      Container(
                          height: 500,
                          width: 600,
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
                          width: 400,
                          margin: EdgeInsets.all(20),
                          padding: EdgeInsets.all(20),
                            decoration: BoxDecoration(
                              color: Colors.teal.shade100,
                              borderRadius: BorderRadius.circular(10),
                          ),
                          child: Column(
                            children: [
                              ElevatedButton.icon(
                                onPressed: (){
                                  showSearch(context: context, delegate: MySearchBar());
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
                                padding: EdgeInsets.all(8),
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

class MySearchBar extends SearchDelegate{
  List<String> stockResultsList = [
    'Google',
    'Tesla',
    'Microsoft'
  ];

  @override
  Widget? buildLeading(BuildContext context) => IconButton(
    icon: Icon(Icons.arrow_back),
    onPressed: (){
      close(context, null);
    },
  );

  @override
  List<Widget> buildActions(BuildContext context) => [
    IconButton(
      icon: Icon(Icons.clear),
      onPressed: (){
        if(query.isEmpty){
          close(context, null);
        }
        else{
          query = '';
        }
      },
    ),
  ];

  @override
  Widget buildResults(BuildContext context) => Center(
    child: Text(
      query
    ),
  );

  @override
  Widget buildSuggestions(BuildContext context) {
    List<String> suggestions = stockResultsList.where((stockResultsList){
      final result = stockResultsList.toLowerCase();
      final input = query.toLowerCase();
      return result.contains(input);
    }).toList();
    
    return ListView.builder(
      itemCount: suggestions.length,
      itemBuilder: (context, index){
        final suggestion = suggestions[index];

        return ListTile(
          title: Text(suggestion),
          onTap: (){
            print("selected suggestion");
            query = suggestion;
            close(context, null);
            //showResults(context);
          }
        );
      },
    ); 
  }
}
