# from graph.nodes.integrate_changes import integrate_changes
#
#
# def test_does_not_modify_state_when_no_repository():
#     state = {
#         "intent": [
#             {
#                 "intent": "add_aggregate",
#                 "target": "Person",
#                 "details": {
#                     "properties": [{"name": "Nickname", "type": "string"}]
#                 }
#             }
#         ]
#     }
#
#     updated_state = integrate_changes(state.copy())
#     assert updated_state == state, "State should not change without a matching repository"
#
#
# def test_adds_missing_property_from_repository_method():
#     state = {
#         "intent": [
#             {
#                 "intent": "add_aggregate",
#                 "target": "Person",
#                 "details": {
#                     "properties": [{"name": "Nickname", "type": "string"}]
#                 }
#             },
#             {
#                 "intent": "add_repository",
#                 "target": "Person",
#                 "details": {
#                     "custom_methods": [
#                         {
#                             "name": "FindByAgeAsync",
#                             "parameters": [{"name": "age", "type": "int"}]
#                         },
#                         {
#                             "name": "GetByNicknameAsync",
#                             "parameters": [{"name": "nickname", "type": "string"}]
#                         }
#                     ]
#                 }
#             }
#         ]
#     }
#
#     updated_state = integrate_changes(state.copy())
#
#     # Fetch updated aggregate
#     person_agg = next(
#         i for i in updated_state["intent"]
#         if i["intent"] == "add_aggregate" and i["target"] == "Person"
#     )
#     props = {p["name"]: p for p in person_agg["details"]["properties"]}
#
#     assert "Nickname" in props, "Original property 'Nickname' should still exist"
#     assert "Age" in props, "Missing property 'Age' should be added from FindByAgeAsync"
#     assert props["Age"]["type"] == "int", "Type should be inferred from method parameters"
#     assert len(props) == 2, "Should contain exactly 2 properties with no duplicates"
#
#
# def test_skips_already_existing_properties():
#     state = {
#         "intent": [
#             {
#                 "intent": "add_aggregate",
#                 "target": "User",
#                 "details": {
#                     "properties": [{"name": "Email", "type": "string"}]
#                 }
#             },
#             {
#                 "intent": "add_repository",
#                 "target": "User",
#                 "details": {
#                     "custom_methods": [
#                         {
#                             "name": "GetByEmailAsync",
#                             "parameters": [{"name": "email", "type": "string"}]
#                         },
#                         {
#                             "name": "FindByAgeAsync",
#                             "parameters": [{"name": "age", "type": "int"}]
#                         }
#                     ]
#                 }
#             }
#         ]
#     }
#
#     updated_state = integrate_changes(state.copy())
#
#     user_agg = next(
#         i for i in updated_state["intent"]
#         if i["intent"] == "add_aggregate" and i["target"] == "User"
#     )
#     props = {p["name"]: p for p in user_agg["details"]["properties"]}
#
#     assert "Email" in props, "Should keep existing property"
#     assert "Age" in props, "Should add inferred property from query method"
#     assert props["Age"]["type"] == "int", "Inferred type should be 'int'"
#     assert len(props) == 2, "Should not duplicate already existing properties"
