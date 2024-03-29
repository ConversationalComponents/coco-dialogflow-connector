# CoCo Dialogflow Connector

CoCo dialog flow connector is a [Flask](http://flask.palletsprojects.com/en/1.1.x/ "Flask") application which allows you to expose your [Dialogflow](https://dialogflow.cloud.google.com/ "Dialw") bots as a components at the [CoCo marketplace](https://marketplace.conversationalcomponents.com/ "CoCo marketplace").

### Deployment Flow:

1. Create a bot on Dialogflow.
2. Create 3 actions at your conversation flow:
	- **Done Action** - Action which will be triggered when the bot/`component` achived it's goal(Default: input.complete).
	- **Failed Action** - Action which will be triggered when the bot/`component` will not complete it's goad(Default: input.failed).  
	- **Out Of Context** - Action which will be triggered when the conversation went out of context(input.unknown).
3. Create private key for bot/`component`  service account in JSON format.
4. Place the key JSON at the following directory at the CoCo DialogFlow Connector source:
`/DialogFlowManager/components` - Each file represent a component which can be accessed through an http call to` https://<host>/api/exchange/<file name - no extension>/<session ID>`
5. Map the 3 actions that were created at the config or just use the default action names which are mentioned above.
6. Upload the Flask app to a cloud service(Google app engine is recommende - yaml file included.)



#### 1. Create a bot on Dialogflow.

 ![Create a new agent.](/Screenshots/1CreateBot.png)

 Create a new agent.

 #### 2. Create 3 actions at your conversation flow.

 ![Create relevant action.](/Screenshots/2CreateActions.png)

 At the example the created action will complete the component.

 #### 3. Create private key for bot/`component`  service account in JSON format.

 ![Create key for service account.](/Screenshots/3CreateKeyForServiceAccount.png)
 ![Create key for service account, Create key button.](/Screenshots/4CreateKeyForServiceAccount.png)
 ![Create key for service account, Choose JSON.](/Screenshots/5CreateKeyForServiceAccount.png)


 #### 4. Place the key JSON at the following directory at the CoCo DialogFlow Connector source.

 ![Place component key in connector source directory.](/Screenshots/6PlaceFileInSourceCode2.png)

 #### 5. Map the 3 actions that were created at the config or just use the default action names.

  ![Configure component actions.](/Screenshots/7ConfigComponentsActions.png)

  Map the bot actions to component states at the config.py file.

 #### 6. Upload the Flask app to a cloud service.

 Open bash, configure gcloud tools and then run the following command:

    `gcloud app deploy`


