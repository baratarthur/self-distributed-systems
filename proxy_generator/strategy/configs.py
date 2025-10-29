from helpers.write_component_helper import WriteComponentHelper

strategy_configs = {
    "replicate": {
        "dependencies": [
            { "lib": "util.Random", "alias": "random" },
            { "lib": "data.json.JSONEncoder", "alias": "je" },
            { "lib": "utils.PodCreatorUtil", "alias": "podCreator" }
        ],
        "charachteristics": {
            "weak": [
                lambda file: WriteComponentHelper(file).provide_idented_flow("Response broadcast(Request r)", [
                    "Response res",
                    WriteComponentHelper(file).provide_idented_flow("mutex(pointerLock)", [
                        WriteComponentHelper(file).provide_idented_flow("for(int i = 0; i < remotes.arrayLength; i++)", [
                            "connection.connect(remotes[i])",
                            "res = connection.make(r)"
                        ])
                    ]),
                    "return res"
                ]),
                lambda file: WriteComponentHelper(file).provide_idented_flow("Response anycast(Request r)", [
                    "int i = random.getInt(remotes.arrayLength)",
                    "connection.connect(remotes[i])",
                    "return connection.make(r)"
                ])
            ],
            "strong": [
                lambda file: WriteComponentHelper(file).provide_idented_flow("Response broadcast(Request r)", [
                    "Response res",
                    WriteComponentHelper(file).provide_idented_flow("mutex(pointerLock)", [
                        WriteComponentHelper(file).provide_idented_flow("for(int i = 0; i < remotes.arrayLength; i++)", [
                            "connection.connect(remotes[i])",
                            "res = connection.make(r)"
                        ])
                    ]),
                    "return res"
                ]),
                lambda file: WriteComponentHelper(file).provide_idented_flow("Response anycast(Request r)", [
                     WriteComponentHelper(file).provide_idented_flow("mutex(pointerLock)", [
                        "int i = random.getInt(remotes.arrayLength)",
                        "connection.connect(remotes[i])",
                        "return connection.make(r)"
                    ])
                ])
            ]
        },
        "methods": {
            "change": "broadcast",
            "no_change": "anycast"
        }
    }
}
