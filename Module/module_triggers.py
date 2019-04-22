from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *

from module_constants import *


####################################################################################################################
#  Each trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Delay interval: Time to wait before applying the consequences of the trigger
#    After its conditions have been evaluated as true.
# 3) Re-arm interval. How much time must pass after applying the consequences of the trigger for the trigger to become active again.
#    You can put the constant ti_once here to make sure that the trigger never becomes active again after it fires once.
# 4) Conditions block (list). This must be a valid operation block. See header_operations.py for reference.
#    Every time the trigger is checked, the conditions block will be executed.
#    If the conditions block returns true, the consequences block will be executed.
#    If the conditions block is empty, it is assumed that it always evaluates to true.
# 5) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
####################################################################################################################

# Some constants for use below
merchant_inventory_space = 18
num_merchandise_goods = 36

triggers = [
# Tutorial:
  (0.1, 0, ti_once, [(map_free,0)], [(dialog_box, "str_tutorial_map1")]),

# Refresh Merchants
  # (0.0, 0, 168.0, [], #168
  # [    
    # (call_script, "script_refresh_center_inventories"),
  # ]),

# Refresh Armor sellers
  # (0.0, 0, 168.0, [],
  # [    
    # (call_script, "script_refresh_center_armories"),
  # ]),

# Refresh Weapon sellers
  # (0.0, 0, 168.0, [],
  # [
    # (call_script, "script_refresh_center_weaponsmiths"),
  # ]),

# Refresh Horse sellers
  # (0.0, 0, 168.0, [],
  # [
    # (call_script, "script_refresh_center_stables"),
  # ]),

#############

#Captivity:

#  (1.0, 0, 0.0, [],
#   [
#       (ge, "$captivity_mode",1),
#       (store_current_hours,reg(1)),
#       (val_sub,reg(1), "$captivity_end_time"),
#       (ge,reg(1),0),
#       (display_message, "str_nobleman_reached_destination"),
#       (jump_to_menu, "$captivity_end_menu"),
#    ]),


  # (5.7, 0, 0.0, 
  # [
    #### (store_num_parties_of_template, reg2, "pt_manhunters"),    
    #### (lt, reg2, 4)
  # ],
  # [
    #### (set_spawn_radius, 1),
    #### (store_add, ":p_town_50_plus_one", "p_town_31_3", 1),
    #### (store_random_in_range, ":selected_town", "p_town_1", ":p_town_50_plus_one"),
    #### (spawn_around_party, ":selected_town", "pt_manhunters"),
  # ]),



  (1.0, 0.0, 0.0, [
  (check_quest_active, "qst_track_down_bandits"),
  (neg|check_quest_failed, "qst_track_down_bandits"),
  (neg|check_quest_succeeded, "qst_track_down_bandits"),
  
  ],
   [
    (quest_get_slot, ":bandit_party", "qst_track_down_bandits", slot_quest_target_party),
    (try_begin),
        (party_is_active, ":bandit_party"),
        (store_faction_of_party, ":bandit_party_faction", ":bandit_party"),
        (neg|is_between, ":bandit_party_faction", kingdoms_begin, kingdoms_end), #ie, the party has not respawned as a non-bandit
        
        
        (assign, ":spot_range", 8),
        (try_begin),
            (is_currently_night),
            (assign, ":spot_range", 5),
        (try_end),
        
        (try_for_parties, ":party"),
            (gt, ":party", "p_spawn_points_end"),
            
            (store_faction_of_party, ":faction", ":party"),
            (is_between, ":faction", kingdoms_begin, kingdoms_end),
            
            
            (store_distance_to_party_from_party, ":distance", ":party", ":bandit_party"),
            (lt, ":distance", ":spot_range"),
            (try_begin),
                (eq, "$cheat_mode", 1),
                (str_store_party_name, s4, ":party"),
                (display_message, "@{!}DEBUG -- Wanted bandits spotted by {s4}"),
            (try_end),
            
            (call_script, "script_get_closest_center", ":bandit_party"),
            (assign, ":nearest_center", reg0),
#            (try_begin),
#                (get_party_ai_current_behavior, ":behavior", ":party"),
#                (eq, ":behavior", ai_bhvr_attack_party),
#                (call_script, "script_add_log_entry",  logent_party_chases_wanted_bandits, ":party",  ":nearest_center", ":bandit_party", -1),
#            (else_try),
#                (eq, ":behavior", ai_bhvr_avoid_party),
#                (call_script, "script_add_log_entry",  logent_party_runs_from_wanted_bandits, ":party",  ":nearest_center", ":bandit_party", -1),
#            (else_try),
            (call_script, "script_add_log_entry",  logent_party_spots_wanted_bandits, ":party",  ":nearest_center", ":bandit_party", -1),
#            (try_end),
        (try_end),
    (else_try), #Party not found
        (display_message, "str_bandits_eliminated_by_another"),
        (call_script, "script_abort_quest", "qst_track_down_bandits", 0),
    (try_end),
   ]),


#Tax Collectors
# Prisoner Trains
#  (4.1, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_prisoner_train"),
#                         (assign, "$pin_limit", peak_prisoner_trains),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                         (party_set_ai_behavior, "$pout_party",ai_bhvr_travel_to_party),
#                         (party_set_ai_object, "$pout_party", "$pout_town"),
#                    ]),
#
#  (4.1, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_prisoner_train"),
#                         (assign, "$pin_limit", peak_prisoner_trains),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                         (party_set_ai_behavior, "$pout_party",ai_bhvr_travel_to_party),
#                         (party_set_ai_object, "$pout_party", "$pout_town"),
#                    ]),

  (2.0, 0, 0, [(store_random_party_of_template, reg(2), "pt_prisoner_train_party"),
               (party_is_in_any_town,reg(2)),
               ],
              [(store_faction_of_party, ":faction_no", reg(2)),
               (call_script, "script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
               (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
               (party_set_ai_object,reg(2),reg0),
               (party_set_flags, reg(2), pf_default_behavior, 0),
            ]),

##Caravans
#  (4.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_caravan"),
#                         (assign, "$pin_limit", peak_kingdom_caravans),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                         (party_set_ai_behavior, "$pout_party",ai_bhvr_travel_to_party),
#                         (party_set_ai_object, "$pout_party", "$pout_town"),
#                    ]),

#  (4.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_caravan"),
#                         (assign, "$pin_limit", peak_kingdom_caravans),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                         (party_set_ai_behavior, "$pout_party",ai_bhvr_travel_to_party),
#                         (party_set_ai_object, "$pout_party", "$pout_town"),
#                    ]),

##  (2.0, 0, 0, [(store_random_party_of_template, reg(2), "pt_kingdom_caravan_party"),
##               (party_is_in_any_town,reg(2)),
##               ],
##              [(store_faction_of_party, ":faction_no", reg(2)),
##               (call_script, "script_cf_select_random_town_with_faction", ":faction_no"),
##               (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
##               (party_set_ai_object,reg(2),reg0),
##               (party_set_flags, reg(2), pf_default_behavior, 0),
##            ]),
  
  (4.0, 0, 0.0,
   [
     (eq, "$caravan_escort_state", 1), #cancel caravan_escort_state if caravan leaves the destination
     (assign, ":continue", 0),
     (try_begin),
       (neg|party_is_active, "$caravan_escort_party_id"),
       (assign, ":continue", 1),
     (else_try),
       (get_party_ai_object, ":ai_object", "$caravan_escort_party_id"),
       (neq, ":ai_object", "$caravan_escort_destination_town"),
       (assign, ":continue", 1),
     (try_end),
     (eq, ":continue", 1),
     ],
   [
     (assign, "$caravan_escort_state", 0),
     ]),

#Messengers
#  (4.2, 0, 0.0, [],
#   [(assign, "$pin_faction", "fac_swadians"),
#    (assign, "$pin_party_template", "pt_swadian_messenger"),
#    (assign, "$pin_limit", peak_kingdom_messengers),
#    (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#    (party_set_ai_behavior, "$pout_party",ai_bhvr_travel_to_party),
#    (party_set_ai_object, "$pout_party", "$pout_town"),
#    ]),

#  (4.2, 0, 0.0, [],
#   [(assign, "$pin_faction", "fac_vaegirs"),
#    (assign, "$pin_party_template", "pt_vaegir_messenger"),
#    (assign, "$pin_limit", peak_kingdom_caravans),
#    (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#    (party_set_ai_behavior, "$pout_party",ai_bhvr_travel_to_party),
#    (party_set_ai_object, "$pout_party", "$pout_town"),
#    ]),

  # (1.5, 0, 0,
    # [
      # (store_random_party_of_template, reg(2), "pt_messenger_party"),
      # (party_is_in_any_town,reg(2)),
    # ],
    # [
      # (store_faction_of_party, ":faction_no", reg(2)),
      # (call_script, "script_cf_select_random_walled_center_with_faction", ":faction_no", -1),
      # (party_set_ai_behavior,reg(2),ai_bhvr_travel_to_party),
      # (party_set_ai_object,reg(2),reg0),
      # (party_set_flags, reg(2), pf_default_behavior, 0),
    # ]
  # ),
  
  

#Deserters

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_deserters"),
#                         (assign, "$pin_limit", 4),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),
  
#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_deserters"),
#                         (assign, "$pin_limit", 4),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

    
    
#Swadians
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_swadian_foragers",4)]),
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_swadian_scouts",4)]),
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_swadian_harassers",3)]),
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_swadian_war_parties",2)]),


#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_foragers"),
#                         (assign, "$pin_limit", "$peak_swadian_foragers"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_scouts"),
#                         (assign, "$pin_limit", "$peak_swadian_scouts"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_patrol"),
#                         (assign, "$pin_limit", "$peak_swadian_harassers"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_swadians"),
#                         (assign, "$pin_party_template", "pt_swadian_war_party"),
#                         (assign, "$pin_limit", "$peak_swadian_war_parties"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),
#Vaegirs
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_vaegir_foragers",4)]),
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_vaegir_scouts",4)]),
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_vaegir_harassers",3)]),
#  (0.0, 0.0, ti_once, [], [(assign, "$peak_vaegir_war_parties",2)]),
  

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_foragers"),
#                         (assign, "$pin_limit", "$peak_vaegir_foragers"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_scouts"),
#                         (assign, "$pin_limit", "$peak_vaegir_scouts"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_patrol"),
#                         (assign, "$pin_limit", "$peak_vaegir_harassers"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#  (10.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_vaegirs"),
#                         (assign, "$pin_party_template", "pt_vaegir_war_party"),
#                         (assign, "$pin_limit", "$peak_vaegir_war_parties"),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),

#Villains etc.
#  (14.2, 0, 0.0, [],
#                     [
#                         (assign, "$pin_faction", "fac_sea_raiders"),
#                         (assign, "$pin_party_template", "pt_sea_raiders"),
#                         (assign, "$pin_limit", 5),
#                         (call_script, "script_cf_spawn_party_at_faction_town_if_below_limit"),
#                    ]),


#
##  (10.1, 0, 0.0, [],
##                     [
##                         (assign, "$pin_party_template", "pt_refugees"),
##                         (assign, "$pin_limit", 5),
##                         (call_script, "script_cf_spawn_party_at_random_town_if_below_limit"),
##                    ]),
##
##  (10.1, 0, 0.0, [],
##                     [
##                         (assign, "$pin_party_template", "pt_farmers"),
##                         (assign, "$pin_limit", 6),
##                         (call_script, "script_cf_spawn_party_at_random_town_if_below_limit"),
##                    ]),

#  [1.0, 96.0, ti_once, [], [[assign, "$peak_dark_hunters",3]]],
  
##  (10.1, 0, 0.0, [],
##                     [
##                         (assign, "$pin_party_template", "pt_dark_hunters"),
##                         (assign, "$pin_limit", "$peak_dark_hunters"),
##                         (call_script, "script_cf_spawn_party_at_random_town_if_below_limit"),
##                    ]),

#Companion quests

##  (0, 0, ti_once,
##   [
##       (entering_town, "p_town_1"),
##       (main_party_has_troop, "trp_borcha"),
##       (eq, "$borcha_freed",0)
##    ],
##   
##   [
##       (assign, "$borcha_arrive_sargoth_as_prisoner", 1),
##       (start_map_conversation, "trp_borcha", -1)
##    ]
##   ),
##
##  (1, 0, ti_once,
##   [
##      (map_free,0),
##      (eq, "$borcha_asked_for_freedom",0),
##      (main_party_has_troop, "trp_borcha")
##    ],
##   [
##       (start_map_conversation, "trp_borcha", -1)
##    ]
##   ),
##  
##  (2, 0, ti_once,
##   [
##      (map_free, 0),
##      (neq, "$borcha_asked_for_freedom",0),
##      (eq, "$borcha_freed",0),
##      (main_party_has_troop, "trp_borcha")
##    ],
##   [
##       (start_map_conversation, "trp_borcha", -1),
##    ]
##   ),

##### TODO: QUESTS COMMENT OUT BEGIN

###########################################################################
### Random Governer Quest triggers
###########################################################################

# Incriminate Loyal Advisor quest
  (0.2, 0.0, 0.0,
   [
       (check_quest_active, "qst_incriminate_loyal_commander"),
       (neg|check_quest_concluded, "qst_incriminate_loyal_commander"),
       (quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_current_state, 2),
       (quest_get_slot, ":quest_target_center", "qst_incriminate_loyal_commander", slot_quest_target_center),
       (quest_get_slot, ":quest_target_party", "qst_incriminate_loyal_commander", slot_quest_target_party),
       (try_begin),
         (neg|party_is_active, ":quest_target_party"),
         (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 3),
         (call_script, "script_fail_quest", "qst_incriminate_loyal_commander"),
       (else_try),
         (party_is_in_town, ":quest_target_party", ":quest_target_center"),
         (remove_party, ":quest_target_party"),
         (quest_set_slot, "qst_incriminate_loyal_commander", slot_quest_current_state, 3),
         (quest_get_slot, ":quest_object_troop", "qst_incriminate_loyal_commander", slot_quest_object_troop),
         (assign, ":num_available_factions", 0),
         (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
           (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
           (neq, ":faction_no", "fac_player_supporters_faction"),
           (neg|quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_target_faction, ":faction_no"),
           (val_add, ":num_available_factions", 1),
         (try_end),
         (try_begin),
           (gt, ":num_available_factions", 0),
           (store_random_in_range, ":random_faction", 0, ":num_available_factions"),
           (assign, ":target_faction", -1),
           (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
             (eq, ":target_faction", -1),
             (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
             (neq, ":faction_no", "fac_player_supporters_faction"),
             (neg|quest_slot_eq, "qst_incriminate_loyal_commander", slot_quest_target_faction, ":faction_no"),
             (val_sub, ":random_faction", 1),
             (lt, ":random_faction", 0),
             (assign, ":target_faction", ":faction_no"),
           (try_end),
         (try_end),
         (try_begin),
           (gt, ":target_faction", 0),
           (call_script, "script_change_troop_faction", ":quest_object_troop", ":target_faction"),
         (else_try),
           (call_script, "script_change_troop_faction", ":quest_object_troop", "fac_robber_knights"),
         (try_end),
         (call_script, "script_succeed_quest", "qst_incriminate_loyal_commander"),
       (try_end),
    ],
   []
   ),
# Runaway Peasants quest
  (0.2, 0.0, 0.0,
   [
       (check_quest_active, "qst_bring_back_runaway_serfs"),
       (neg|check_quest_concluded, "qst_bring_back_runaway_serfs"),
       (quest_get_slot, ":quest_object_center", "qst_bring_back_runaway_serfs", slot_quest_object_center),
       (quest_get_slot, ":quest_target_center", "qst_bring_back_runaway_serfs", slot_quest_target_center),
       (try_begin),
         (party_is_active, "$qst_bring_back_runaway_serfs_party_1"),
         (try_begin),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_1", ":quest_target_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_1"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
         (else_try),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_1", ":quest_object_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_1"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_bring_back_runaway_serfs_party_1"),
           (gt, ":cur_distance", 3),
           (party_set_ai_object, "$qst_bring_back_runaway_serfs_party_1", ":quest_target_center"),
         (try_end),
       (try_end),
       (try_begin),
         (party_is_active, "$qst_bring_back_runaway_serfs_party_2"),
         (try_begin),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_2", ":quest_target_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_2"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
         (else_try),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_2", ":quest_object_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_2"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_bring_back_runaway_serfs_party_2"),
           (gt, ":cur_distance", 3),
           (party_set_ai_object, "$qst_bring_back_runaway_serfs_party_2", ":quest_target_center"),
         (try_end),
       (try_end),
       (try_begin),
         (party_is_active, "$qst_bring_back_runaway_serfs_party_3"),
         (try_begin),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_3", ":quest_target_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_3"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_fleed", 1),
         (else_try),
           (party_is_in_town, "$qst_bring_back_runaway_serfs_party_3", ":quest_object_center"),
           (remove_party, "$qst_bring_back_runaway_serfs_party_3"),
           (val_add, "$qst_bring_back_runaway_serfs_num_parties_returned", 1),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_bring_back_runaway_serfs_party_3"),
           (gt, ":cur_distance", 3),
           (party_set_ai_object, "$qst_bring_back_runaway_serfs_party_3", ":quest_target_center"),
         (try_end),
       (try_end),
       (assign, ":sum_removed", "$qst_bring_back_runaway_serfs_num_parties_returned"),
       (val_add, ":sum_removed", "$qst_bring_back_runaway_serfs_num_parties_fleed"),
       (ge, ":sum_removed", 3),
       (try_begin),
         (ge, "$qst_bring_back_runaway_serfs_num_parties_returned", 3),
         (call_script, "script_succeed_quest", "qst_bring_back_runaway_serfs"),
       (else_try),
         (eq, "$qst_bring_back_runaway_serfs_num_parties_returned", 0),
         (call_script, "script_fail_quest", "qst_bring_back_runaway_serfs"),
       (else_try),
         (call_script, "script_conclude_quest", "qst_bring_back_runaway_serfs"),
       (try_end),
    ],
   []
   ),
### Defend Nobles Against Peasants quest
##  (0.2, 0.0, 0.0,
##   [
##       (check_quest_active, "qst_defend_nobles_against_peasants"),
##       (neg|check_quest_succeeded, "qst_defend_nobles_against_peasants"),
##       (neg|check_quest_failed, "qst_defend_nobles_against_peasants"),
##       (quest_get_slot, ":quest_target_center", "qst_defend_nobles_against_peasants", slot_quest_target_center),
##       (assign, ":num_active_parties", 0),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_1", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_1"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_1", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_1"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_1"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_2", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_2"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_2", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_2"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_2"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_3", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_3"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_3", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_3"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_3"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_4", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_4"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_4", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_4"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_4"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_5", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_5"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_5", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_5"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_5"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_6", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_6"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_6", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_6"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_6"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_7", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_7"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_7", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_7"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_7"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_defend_nobles_against_peasants_noble_party_8", 0),
##         (party_is_active, "$qst_defend_nobles_against_peasants_noble_party_8"),
##         (val_add, ":num_active_parties", 1),
##         (party_is_in_town, "$qst_defend_nobles_against_peasants_noble_party_8", ":quest_target_center"),
##         (remove_party, "$qst_defend_nobles_against_peasants_noble_party_8"),
##         (party_get_num_companions, ":num_companions", "$qst_defend_nobles_against_peasants_noble_party_8"),
##         (val_add, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":num_companions"),
##       (try_end),
##       (eq, ":num_active_parties", 0),
##       (try_begin),
##         (store_div, ":limit", "$qst_defend_nobles_against_peasants_num_nobles_to_save", 2),
##         (ge, "$qst_defend_nobles_against_peasants_num_nobles_saved", ":limit"),
##         (call_script, "script_succeed_quest", "qst_defend_nobles_against_peasants"),
##       (else_try),
##         (call_script, "script_fail_quest", "qst_defend_nobles_against_peasants"),
##       (try_end),
##    ],
##   []
##   ),
### Capture Conspirators quest
##  (0.15, 0.0, 0.0,
##   [
##       (check_quest_active, "qst_capture_conspirators"),
##       (neg|check_quest_succeeded, "qst_capture_conspirators"),
##       (neg|check_quest_failed, "qst_capture_conspirators"),
##       (quest_get_slot, ":quest_target_center", "qst_capture_conspirators", slot_quest_target_center),
##       (quest_get_slot, ":faction_no", "qst_capture_conspirators", slot_quest_target_faction),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_num_parties_to_spawn", "$qst_capture_conspirators_num_parties_spawned"),
##         (store_random_in_range, ":random_no", 0, 100),
##         (lt, ":random_no", 20),
##         (set_spawn_radius, 3),
##         (spawn_around_party, ":quest_target_center", "pt_conspirator"),
##         (val_add, "$qst_capture_conspirators_num_parties_spawned", 1),
##         (party_get_num_companions, ":num_companions", reg0),
##         (val_add, "$qst_capture_conspirators_num_troops_to_capture", ":num_companions"),
##         (party_set_ai_behavior, reg0, ai_bhvr_travel_to_party),
##         (party_set_ai_object, reg0, "$qst_capture_conspirators_party_1"),
##         (party_set_flags, reg0, pf_default_behavior, 0),
##         (try_begin),
##           (le, "$qst_capture_conspirators_party_2", 0),
##           (assign, "$qst_capture_conspirators_party_2", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_3", 0),
##           (assign, "$qst_capture_conspirators_party_3", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_4", 0),
##           (assign, "$qst_capture_conspirators_party_4", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_5", 0),
##           (assign, "$qst_capture_conspirators_party_5", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_6", 0),
##           (assign, "$qst_capture_conspirators_party_6", reg0),
##         (else_try),
##           (le, "$qst_capture_conspirators_party_7", 0),
##           (assign, "$qst_capture_conspirators_party_7", reg0),
##         (try_end),
##       (try_end),
##
##       (assign, ":num_active_parties", 0),
##
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_1", 0),
##         (party_is_active, "$qst_capture_conspirators_party_1"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_1"),
##           (remove_party, "$qst_capture_conspirators_party_1"),
##         (else_try),
##           (party_get_num_attached_parties, ":num_attachments", "$qst_capture_conspirators_party_1"),
##           (gt, ":num_attachments", 0),
##           (assign, ":leave_meeting", 0),
##           (try_begin),
##             (store_sub, ":required_attachments", "$qst_capture_conspirators_num_parties_to_spawn", 1),
##             (eq, ":num_attachments", ":required_attachments"),
##             (val_add, "$qst_capture_conspirators_leave_meeting_counter", 1),
##             (ge, "$qst_capture_conspirators_leave_meeting_counter", 15),
##             (assign, ":leave_meeting", 1),
##           (try_end),
##           (try_begin),
##             (eq, "$qst_capture_conspirators_num_parties_to_spawn", "$qst_capture_conspirators_num_parties_spawned"),
##             (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_capture_conspirators_party_1"),
##             (assign, ":min_distance", 3),
##             (try_begin),
##               (is_currently_night),
##               (assign, ":min_distance", 2),
##             (try_end),
##             (lt, ":cur_distance", ":min_distance"),
##             (assign, "$qst_capture_conspirators_leave_meeting_counter", 15),
##             (assign, ":leave_meeting", 1),
##           (try_end),
##           (eq, ":leave_meeting", 1),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_travel_to_point),
##           (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_1"),
##           (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##           (party_set_ai_target_position, "$qst_capture_conspirators_party_1", pos2),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_2", 0),
##             (party_detach, "$qst_capture_conspirators_party_2"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_2", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_2", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_2", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_3", 0),
##             (party_detach, "$qst_capture_conspirators_party_3"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_3", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_3", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_3", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_4", 0),
##             (party_detach, "$qst_capture_conspirators_party_4"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_4", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_4", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_4", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_5", 0),
##             (party_detach, "$qst_capture_conspirators_party_5"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_5", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_5", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_5", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_6", 0),
##             (party_detach, "$qst_capture_conspirators_party_6"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_6", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_6", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_6", pos2),
##           (try_end),
##           (try_begin),
##             (gt, "$qst_capture_conspirators_party_7", 0),
##             (party_detach, "$qst_capture_conspirators_party_7"),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_7", ai_bhvr_travel_to_point),
##             (party_set_flags, "$qst_capture_conspirators_party_7", pf_default_behavior, 0),
##             (call_script, "script_map_get_random_position_around_position_within_range", 15, 17),
##             (party_set_ai_target_position, "$qst_capture_conspirators_party_7", pos2),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_1"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_1"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_1"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_1", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_1", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_1", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_1", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_2", 0),
##         (party_is_active, "$qst_capture_conspirators_party_2"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_2"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_2", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_2"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_2"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_2", ai_bhvr_hold),
##             (party_attach_to_party, "$qst_capture_conspirators_party_2", "$qst_capture_conspirators_party_1"),
##             (party_set_flags, "$qst_capture_conspirators_party_2", pf_default_behavior, 0),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_2"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_2"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_2"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_2", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_2", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_2", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_2", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_3", 0),
##         (party_is_active, "$qst_capture_conspirators_party_3"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_3"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_3", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_3"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_3"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_3", ai_bhvr_hold),
##             (party_attach_to_party, "$qst_capture_conspirators_party_3", "$qst_capture_conspirators_party_1"),
##             (party_set_flags, "$qst_capture_conspirators_party_3", pf_default_behavior, 0),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_3"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_3"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_3"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_3", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_3", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_3", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_3", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_4", 0),
##         (party_is_active, "$qst_capture_conspirators_party_4"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_4"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_4", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_4"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_4"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_4", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_4", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_4", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_4"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_4"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_4"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_4", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_4", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_4", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_4", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_5", 0),
##         (party_is_active, "$qst_capture_conspirators_party_5"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_5"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_5", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_5"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_5"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_5", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_5", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_5", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_5"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_5"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_5"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_5", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_5", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_5", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_5", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_6", 0),
##         (party_is_active, "$qst_capture_conspirators_party_6"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_6"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_6", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_6"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_6"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_6", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_6", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_6", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_6"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_6"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_6"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_6", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_6", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_6", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_6", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##       (try_begin),
##         (gt, "$qst_capture_conspirators_party_7", 0),
##         (party_is_active, "$qst_capture_conspirators_party_7"),
##         (val_add, ":num_active_parties", 1),
##         (try_begin),
##           (party_is_in_any_town, "$qst_capture_conspirators_party_7"),
##           (try_begin),
##             (neg|party_is_in_town, "$qst_capture_conspirators_party_7", "$qst_capture_conspirators_party_1"),
##             (remove_party, "$qst_capture_conspirators_party_7"),
##           (else_try),
##             (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_7"),
##             (neq, ":ai_behavior", ai_bhvr_hold),
##             (party_set_ai_behavior, "$qst_capture_conspirators_party_7", ai_bhvr_hold),
##             (party_set_flags, "$qst_capture_conspirators_party_7", pf_default_behavior, 0),
##             (party_attach_to_party, "$qst_capture_conspirators_party_7", "$qst_capture_conspirators_party_1"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (get_party_ai_behavior, ":ai_behavior", "$qst_capture_conspirators_party_7"),
##           (eq, ":ai_behavior", ai_bhvr_travel_to_point),
##           (party_get_ai_target_position, pos2, "$qst_capture_conspirators_party_7"),
##           (party_get_position, pos1, "$qst_capture_conspirators_party_7"),
##           (get_distance_between_positions, ":distance", pos2, pos1),
##           (lt, ":distance", 200),
##           (call_script, "script_get_closest_walled_center_of_faction", "$qst_capture_conspirators_party_7", ":faction_no"),#Can fail
##           (ge, reg0, 0),
##           (party_set_ai_object, "$qst_capture_conspirators_party_7", reg0),
##           (party_set_ai_behavior, "$qst_capture_conspirators_party_7", ai_bhvr_travel_to_party),
##           (party_set_flags, "$qst_capture_conspirators_party_7", pf_default_behavior, 0),
##         (try_end),
##       (try_end),
##
##       (eq, ":num_active_parties", 0),
##       (party_count_prisoners_of_type, ":count_captured_conspirators", "p_main_party", "trp_conspirator"),
##       (party_count_prisoners_of_type, ":count_captured_conspirator_leaders", "p_main_party", "trp_conspirator_leader"),
##       (val_add, ":count_captured_conspirators", ":count_captured_conspirator_leaders"),
##       (try_begin),
##         (store_div, ":limit", "$qst_capture_conspirators_num_troops_to_capture", 2),
##         (gt, ":count_captured_conspirators", ":limit"),
##         (call_script, "script_succeed_quest", "qst_capture_conspirators"),
##       (else_try),
##         (call_script, "script_fail_quest", "qst_capture_conspirators"),
##       (try_end),
##    ],
##   []
##   ),
# Follow Spy quest
  (0.5, 0.0, 0.0,
   [
       (check_quest_active, "qst_follow_spy"),
       (eq, "$qst_follow_spy_no_active_parties", 0),
       (quest_get_slot, ":quest_giver_center", "qst_follow_spy", slot_quest_giver_center),
       (quest_get_slot, ":quest_object_center", "qst_follow_spy", slot_quest_object_center),
       (assign, ":abort_meeting", 0),
       (try_begin),
         (this_or_next|ge, "$qst_follow_spy_run_away", 2),
         (this_or_next|neg|party_is_active, "$qst_follow_spy_spy_party"),
         (neg|party_is_active, "$qst_follow_spy_spy_partners_party"),
       (else_try),
         (eq, "$qst_follow_spy_meeting_state", 0),
         (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_follow_spy_spy_party"),
         (try_begin),
           (assign, ":min_distance", 3),
           (try_begin),
             (is_currently_night),
             (assign, ":min_distance", 1),
           (try_end),
           (le, ":cur_distance", ":min_distance"),
           (store_distance_to_party_from_party, ":player_distance_to_quest_giver_center", "p_main_party", ":quest_giver_center"),
           (gt, ":player_distance_to_quest_giver_center", 1),
           (val_add, "$qst_follow_spy_run_away", 1),
           (try_begin),
             (eq, "$qst_follow_spy_run_away", 2),
           (assign, ":abort_meeting", 1),
           (display_message, "str_qst_follow_spy_noticed_you"),
           (try_end),
         (else_try),
           (store_distance_to_party_from_party, ":cur_distance", "$qst_follow_spy_spy_partners_party", "$qst_follow_spy_spy_party"),
           (le, ":cur_distance", 1),
           (party_attach_to_party, "$qst_follow_spy_spy_party", "$qst_follow_spy_spy_partners_party"),
           (assign, "$qst_follow_spy_meeting_state", 1),
           (assign, "$qst_follow_spy_meeting_counter", 0),
         (try_end),
       (else_try),
         (eq, "$qst_follow_spy_meeting_state", 1),
         (store_distance_to_party_from_party, ":cur_distance", "p_main_party", "$qst_follow_spy_spy_partners_party"),
         (try_begin),
           (le, ":cur_distance", 1),
           (party_detach, "$qst_follow_spy_spy_party"),
           (val_add, "$qst_follow_spy_run_away", 1),
           (try_begin),
             (eq, "$qst_follow_spy_run_away", 2),
           (assign, ":abort_meeting", 1),
           (display_message, "str_qst_follow_spy_noticed_you"),
           (try_end),
         (else_try),
           (val_add, "$qst_follow_spy_meeting_counter", 1),
           (gt, "$qst_follow_spy_meeting_counter", 4),
           (party_detach, "$qst_follow_spy_spy_party"),
           (assign, ":abort_meeting", 1),
           (assign, "$qst_follow_spy_meeting_state", 2),
         (try_end),
       (try_end),
       (try_begin),
         (eq, ":abort_meeting", 1),
         (party_set_ai_object, "$qst_follow_spy_spy_party", ":quest_giver_center"),
         
         (party_set_ai_object, "$qst_follow_spy_spy_partners_party", ":quest_object_center"),
         
         (party_set_ai_behavior, "$qst_follow_spy_spy_party", ai_bhvr_travel_to_party),
         (party_set_ai_behavior, "$qst_follow_spy_spy_partners_party", ai_bhvr_travel_to_party),
         (party_set_flags, "$qst_follow_spy_spy_party", pf_default_behavior, 0),
         (party_set_flags, "$qst_follow_spy_spy_partners_party", pf_default_behavior, 0),
       (try_end),
       (assign, ":num_active", 0),
       (try_begin),
         (party_is_active, "$qst_follow_spy_spy_party"),
         (val_add, ":num_active", 1),
         (party_is_in_town, "$qst_follow_spy_spy_party", ":quest_giver_center"),
         (remove_party, "$qst_follow_spy_spy_party"),
         (assign, "$qst_follow_spy_spy_back_in_town", 1),
         (val_sub, ":num_active", 1),
       (try_end),
       (try_begin),
         (party_is_active, "$qst_follow_spy_spy_partners_party"),
         (val_add, ":num_active", 1),
         (party_is_in_town, "$qst_follow_spy_spy_partners_party", ":quest_object_center"),
         (remove_party, "$qst_follow_spy_spy_partners_party"),
         (assign, "$qst_follow_spy_partner_back_in_town", 1),
         (val_sub, ":num_active", 1),
       (try_end),
       (try_begin),
         (eq, "$qst_follow_spy_partner_back_in_town",1),
         (eq, "$qst_follow_spy_spy_back_in_town",1),
         (call_script, "script_fail_quest", "qst_follow_spy"),
       (try_end),
       (try_begin),
         (eq, ":num_active", 0),
         (assign, "$qst_follow_spy_no_active_parties", 1),
         (party_count_prisoners_of_type, ":num_spies", "p_main_party", "trp_spy"),
         (party_count_prisoners_of_type, ":num_spy_partners", "p_main_party", "trp_spy_partner"),
         (gt, ":num_spies", 0),
         (gt, ":num_spy_partners", 0),
         (call_script, "script_succeed_quest", "qst_follow_spy"),
       (try_end),
    ],
   []
   ),
### Raiders quest
##  (0.95, 0.0, 0.2,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##    ],
##   [
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
##       (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##    ]
##   ),
##
##  (0.7, 0, 0.2,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##    ],
##   [
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (party_set_ai_behavior, ":quest_target_party",ai_bhvr_travel_to_party),
##       (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
##    ]
##   ),
##  
##  (0.1, 0.0, 0.0,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (neg|party_is_active, ":quest_target_party")
##    ],
##   [
##       (call_script, "script_succeed_quest", "qst_hunt_down_raiders"),
##    ]
##   ),
##  
##  (1.3, 0, 0.0,
##   [
##       (check_quest_active, "qst_hunt_down_raiders"),
##       (neg|check_quest_succeeded, "qst_hunt_down_raiders"),
##       (neg|check_quest_failed, "qst_hunt_down_raiders"),
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (quest_get_slot, ":quest_target_center", "qst_hunt_down_raiders", slot_quest_target_center),
##       (party_is_in_town, ":quest_target_party", ":quest_target_center")
##    ],
##   [
##       (call_script, "script_fail_quest", "qst_hunt_down_raiders"),
##       (display_message, "str_raiders_reached_base"),
##       (quest_get_slot, ":quest_target_party", "qst_hunt_down_raiders", slot_quest_target_party),
##       (remove_party, ":quest_target_party"),
##    ]
##   ),

##### TODO: QUESTS COMMENT OUT END

#########################################################################
# Random MERCHANT quest triggers
####################################  
 # Apply interest to merchants guild debt  1% per week
  (24.0 * 7, 0.0, 0.0,
   [],
   [
       (val_mul, "$debt_to_merchants_guild",101),
       (val_div, "$debt_to_merchants_guild",100)
    ]
   ),
# Escort merchant caravan:
  (0.1, 0.0, 0.1, [(check_quest_active, "qst_escort_merchant_caravan"),
                   (eq, "$escort_merchant_caravan_mode", 1)
                   ],
                  [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                   (try_begin),
                     (party_is_active, ":quest_target_party"),
                     (party_set_ai_behavior, ":quest_target_party", ai_bhvr_hold),
                     (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                   (try_end),
                   ]),
  (0.1, 0.0, 0.1, [(check_quest_active, "qst_escort_merchant_caravan"),
                    (eq, "$escort_merchant_caravan_mode", 0),
                    ],
                   [(quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                    (try_begin),
                      (party_is_active, ":quest_target_party"),
                      (party_set_ai_behavior, ":quest_target_party", ai_bhvr_escort_party),
                      (party_set_flags, ":quest_target_party", pf_default_behavior, 0),
                      (party_set_ai_object, ":quest_target_party", "p_main_party"),
                    (try_end),
                    ]),

  (0.1, 0, 0.0, [(check_quest_active, "qst_escort_merchant_caravan"),
                 (quest_get_slot, ":quest_target_party", "qst_escort_merchant_caravan", slot_quest_target_party),
                 (neg|party_is_active, ":quest_target_party"),
                 ],
                [(call_script, "script_abort_quest", "qst_escort_merchant_caravan", 2),
                 ]),

# Troublesome bandits
  (0.3, 0.0, 1.1, [(check_quest_active, "qst_troublesome_bandits"),
                   (neg|check_quest_failed, "qst_troublesome_bandits"),
                   (store_num_parties_destroyed, ":cur_eliminated", "pt_troublesome_bandits"),
                   (lt, "$qst_troublesome_bandits_eliminated", ":cur_eliminated"),
                   (store_num_parties_destroyed_by_player, ":cur_eliminated_by_player", "pt_troublesome_bandits"),
                   (eq, ":cur_eliminated_by_player", "$qst_troublesome_bandits_eliminated_by_player"),
                   ],
                  [(display_message, "str_bandits_eliminated_by_another"),
                   (call_script, "script_abort_quest", "qst_troublesome_bandits", 2),
                   ]),

  (0.3, 0.0, 1.1, [(check_quest_active, "qst_troublesome_bandits"),
                   (neg|check_quest_succeeded, "qst_troublesome_bandits"),
                   (store_num_parties_destroyed, ":cur_eliminated", "pt_troublesome_bandits"),
                   (lt, "$qst_troublesome_bandits_eliminated", ":cur_eliminated"),
                   (store_num_parties_destroyed_by_player, ":cur_eliminated_by_player", "pt_troublesome_bandits"),
                   (neq, ":cur_eliminated_by_player", "$qst_troublesome_bandits_eliminated_by_player"),
                   ],
                  [(call_script, "script_succeed_quest", "qst_troublesome_bandits"),]),
                  
# Kidnapped girl:
   (1, 0, 0,
   [(check_quest_active, "qst_kidnapped_girl"),
    (quest_get_slot, ":quest_target_party", "qst_kidnapped_girl", slot_quest_target_party),
    (party_is_active, ":quest_target_party"),
    (party_is_in_any_town, ":quest_target_party"),
    (remove_party, ":quest_target_party"),
    ],
   []
   ),


#Rebellion changes begin
#move 

  (0, 0, 24 * 14,
   [
    (try_for_range, ":pretender", pretenders_begin, pretenders_end),
      (troop_set_slot, ":pretender", slot_troop_cur_center, 0),
      (neq, ":pretender", "$supported_pretender"),
      (troop_get_slot, ":target_faction", ":pretender", slot_troop_original_faction),
      (faction_slot_eq, ":target_faction", slot_faction_state, sfs_active),
      (faction_slot_eq, ":target_faction", slot_faction_has_rebellion_chance, 1),
      (neg|troop_slot_eq, ":pretender", slot_troop_occupation, slto_kingdom_hero),

      (try_for_range, ":unused", 0, 30),
        (troop_slot_eq, ":pretender", slot_troop_cur_center, 0),
        (store_random_in_range, ":town", towns_begin, towns_end),
        (store_faction_of_party, ":town_faction", ":town"),
        (store_relation, ":relation", ":town_faction", ":target_faction"),
        (le, ":relation", 0), #fail if nothing qualifies
       
        (troop_set_slot, ":pretender", slot_troop_cur_center, ":town"),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_troop_name, 4, ":pretender"),
          (str_store_party_name, 5, ":town"),
          (display_message, "@{!}{s4} is in {s5}"),
        (try_end),
      (try_end),

#        (try_for_range, ":rebel_faction", rebel_factions_begin, rebel_factions_end),
#            (faction_get_slot, ":rebellion_status", ":rebel_faction", slot_faction_state),
#            (eq, ":rebellion_status", sfs_inactive_rebellion),
#            (faction_get_slot, ":pretender", ":rebel_faction", slot_faction_leader),
#            (faction_get_slot, ":target_faction", ":rebel_faction", slot_faction_rebellion_target),#

#            (store_random_in_range, ":town", towns_begin, towns_end),
#            (store_faction_of_party, ":town_faction", ":town"),
#            (store_relation, ":relation", ":town_faction", ":target_faction"),
#            (le, ":relation", 0), #fail if nothing qualifies

 #           (faction_set_slot, ":rebel_faction", slot_faction_inactive_leader_location, ":town"),
        (try_end), 
       ],
[]
),
#Rebellion changes end

#NPC system changes begin
#Move unemployed NPCs around taverns
   (24 * 15 , 0, 0, 
   [
    (call_script, "script_update_companion_candidates_in_taverns"),
    ],
   []
   ),

#Process morale and determine personality clashes
  (0, 0, 24,
   [],
[
#Count NPCs in party and get the "grievance divisor", which determines how fast grievances go away
#Set their relation to the player
        (assign, ":npcs_in_party", 0),
        (assign, ":grievance_divisor", 100),
        (try_for_range, ":npc1", companions_begin, companions_end),
            (main_party_has_troop, ":npc1"),
            (val_add, ":npcs_in_party", 1),
        (try_end),
        (val_sub, ":grievance_divisor", ":npcs_in_party"),
        (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
        (val_add, ":grievance_divisor", ":persuasion_level"),
        (assign, reg7, ":grievance_divisor"),

#        (display_message, "@{!}Process NPC changes. GD: {reg7}"),



##Activate personality clash from 24 hours ago
        (try_begin), #scheduled personality clashes require at least 24hrs together
             (gt, "$personality_clash_after_24_hrs", 0),
             (eq, "$disable_npc_complaints", 0),
             (try_begin),
                  (troop_get_slot, ":other_npc", "$personality_clash_after_24_hrs", slot_troop_personalityclash_object),
                  (main_party_has_troop, "$personality_clash_after_24_hrs"),
                  (main_party_has_troop, ":other_npc"),
                  (assign, "$npc_with_personality_clash", "$personality_clash_after_24_hrs"),
             (try_end),
             (assign, "$personality_clash_after_24_hrs", 0),
        (try_end),
#


        (try_for_range, ":npc", companions_begin, companions_end),
###Reset meeting variables
            (troop_set_slot, ":npc", slot_troop_turned_down_twice, 0),
            (try_begin),
                (troop_slot_eq, ":npc", slot_troop_met, 1),
                (troop_set_slot, ":npc", slot_troop_met_previously, 1),
            (try_end),

###Check for coming out of retirement
            (troop_get_slot, ":occupation", ":npc", slot_troop_occupation),
            (try_begin),
                (eq, ":occupation", slto_retirement),
                (troop_get_slot, ":renown_min", ":npc", slot_troop_return_renown),

                (str_store_troop_name, s31, ":npc"),
                (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
                (assign, reg4, ":player_renown"),
                (assign, reg5, ":renown_min"),
#                (display_message, "@{!}Test {s31}  for retirement return {reg4}, {reg5}."),

                (gt, ":player_renown", ":renown_min"),
                (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, 0),
                (troop_set_slot, ":npc", slot_troop_morality_penalties, 0),
                (troop_set_slot, ":npc", slot_troop_occupation, 0),
            (try_end),


#Check for political issues
            (try_begin), #does npc's opponent pipe up?
                (troop_slot_ge, ":npc", slot_troop_days_on_mission, 5),
                (troop_slot_eq, ":npc", slot_troop_current_mission, npc_mission_kingsupport),

                (troop_get_slot, ":other_npc", ":npc", slot_troop_kingsupport_opponent),
                (troop_slot_eq, ":other_npc", slot_troop_kingsupport_objection_state, 0),

                (troop_set_slot, ":other_npc", slot_troop_kingsupport_objection_state, 1),

                (str_store_troop_name, s3, ":npc"),
                (str_store_troop_name, s4, ":other_npc"),

                (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "str_s4_ready_to_voice_objection_to_s3s_mission_if_in_party"),
                (try_end),
            (try_end),

            #Check for quitting
            (try_begin),
                (main_party_has_troop, ":npc"),
                (eq, "$disable_npc_complaints", 0),
                (call_script, "script_npc_morale", ":npc"),
                (assign, ":npc_morale", reg0),
                
                (try_begin),
                    (lt, ":npc_morale", 20),
                    (store_random_in_range, ":random", 0, 100),
                    (val_add, ":npc_morale", ":random"),
                    (lt, ":npc_morale", 20),
                    (assign, "$npc_is_quitting", ":npc"),
                (try_end),                

                #Reduce grievance over time (or augment, if party is overcrowded
                (troop_get_slot, ":grievance", ":npc", slot_troop_personalityclash_penalties),
                (val_mul, ":grievance", 90),
                (val_div, ":grievance", ":grievance_divisor"),
                (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, ":grievance"),

                (troop_get_slot, ":grievance", ":npc", slot_troop_morality_penalties),
                (val_mul, ":grievance", 90),
                (val_div, ":grievance", ":grievance_divisor"),
                (troop_set_slot, ":npc", slot_troop_morality_penalties, ":grievance"),


                #Change personality grievance levels
                (try_begin),
                    (this_or_next|troop_slot_ge, ":npc", slot_troop_personalityclash_state, 1),
                        (eq, "$disable_npc_complaints", 1),
                    (troop_get_slot, ":object", ":npc", slot_troop_personalityclash_object),
                    (main_party_has_troop, ":object"),
                    (call_script, "script_reduce_companion_morale_for_clash", ":npc", ":object", slot_troop_personalityclash_state),
                (try_end),
                (try_begin),
                    (this_or_next|troop_slot_ge, ":npc", slot_troop_personalityclash2_state, 1),
                        (eq, "$disable_npc_complaints", 1),
                    (troop_get_slot, ":object", ":npc", slot_troop_personalityclash2_object),
                    (main_party_has_troop, ":object"),
                    (call_script, "script_reduce_companion_morale_for_clash", ":npc", ":object", slot_troop_personalityclash2_state),
                (try_end),
                (try_begin),
                    (this_or_next|troop_slot_ge, ":npc", slot_troop_personalitymatch_state, 1),
                        (eq, "$disable_npc_complaints", 1),
                    (troop_get_slot, ":object", ":npc", slot_troop_personalitymatch_object),
                    (main_party_has_troop, ":object"),
                    (troop_get_slot, ":grievance", ":npc", slot_troop_personalityclash_penalties),
                    (val_mul, ":grievance", 9),
                    (val_div, ":grievance", 10),
                    (troop_set_slot, ":npc", slot_troop_personalityclash_penalties, ":grievance"),
                (try_end),



#Check for new personality clashes

                #Active personality clash 1 if at least 24 hours have passed
                (try_begin),
                    (eq, "$disable_npc_complaints", 0),
                    (eq, "$npc_with_personality_clash", 0),
                    (eq, "$npc_with_personality_clash_2", 0),
                    (eq, "$personality_clash_after_24_hrs", 0),
                    (troop_slot_eq, ":npc", slot_troop_personalityclash_state, 0),
                    (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash_object),
                    (main_party_has_troop, ":other_npc"),
                    (assign, "$personality_clash_after_24_hrs", ":npc"),
                (try_end),

                #Personality clash 2 and personality match is triggered by battles
                (try_begin),
                    (eq, "$npc_with_political_grievance", 0),

                    (troop_slot_eq, ":npc", slot_troop_kingsupport_objection_state, 1),
                    (assign, "$npc_with_political_grievance", ":npc"),
                (try_end),

            #main party does not have troop, and the troop is a companion
            (else_try),
                (neg|main_party_has_troop, ":npc"),
                (eq, ":occupation", slto_player_companion),

                (troop_get_slot, ":days_on_mission", ":npc", slot_troop_days_on_mission),

                (try_begin), #debug
                    (eq, "$cheat_mode", 1),
                    (str_store_troop_name, s10, ":npc"),
                    (assign, reg0, ":days_on_mission"),
                    (display_message, "@Checking rejoin of {s10} days on mission: {reg0}"),
                (try_end),

                (try_begin),
                    (gt, ":days_on_mission", 0),
                    (val_sub, ":days_on_mission", 1),
                    (troop_set_slot, ":npc", slot_troop_days_on_mission, ":days_on_mission"),
                ##diplomacy begin
                (else_try),
                  (troop_slot_eq, ":npc", slot_troop_current_mission, dplmc_npc_mission_spy_request), #spy mission
                  (troop_slot_ge, ":npc", dplmc_slot_troop_mission_diplomacy, 1), #caught

                  (troop_set_slot, "trp_merc_euro_spearman", slot_troop_mission_object, ":npc"),
                  (assign, "$npc_to_rejoin_party", "trp_merc_euro_spearman"),
                ##diplomacy end
                (else_try),
                    (troop_slot_ge, ":npc", slot_troop_current_mission, 1),

                    #If the hero can join
                    (this_or_next|neg|troop_slot_eq, ":npc", slot_troop_current_mission, npc_mission_rejoin_when_possible),
                    (hero_can_join, ":npc"),

                    (assign, "$npc_to_rejoin_party", ":npc"),
                (try_end),
            (try_end),
        (try_end),
    ]),




#NPC system changes end

 (0.5, 0, 0.0, [(eq, "$tom_use_longships", 1)],
[

  (try_for_parties, ":cur_party"),
    (neg|is_between, centers_begin, centers_end),
    (party_get_template_id, ":cur_template", ":cur_party"),
    (neq, ":cur_template", "pt_manor"),
    (gt, ":cur_template", 0),
    (party_get_icon, ":icon", ":cur_party"),
    (try_begin),
      (call_script, "script_cf_is_party_on_water", ":cur_party"),
      (neg | is_between, ":icon", "icon_longship", "icon_bandit_marker"),
      (try_begin), #set the original icon to slot
        (party_slot_eq, ":cur_party", party_slot_original_icon, 0),
        (party_set_slot, ":cur_party", party_slot_original_icon, ":icon"),
      (try_end),
      (store_faction_of_party, ":faction", ":cur_party"),
      (try_begin),      
        (eq, ":faction", "fac_kingdom_5"),
        (party_set_icon, ":cur_party", "icon_longship_poland"),
      (else_try),
        (eq, ":faction", "fac_kingdom_1"),
        (party_set_icon, ":cur_party", "icon_longship_teu"),
      (else_try),
        (eq, ":faction", "fac_kingdom_2"),
        (party_set_icon, ":cur_party", "icon_longship_lithuania"),
      (else_try),
        (eq, ":faction", "fac_kingdom_3"),
        (party_set_icon, ":cur_party", "icon_longship_mongol"),
      (else_try),
        (eq, ":faction", "fac_kingdom_4"),
        (party_set_icon, ":cur_party", "icon_longship_denmark"),
      (else_try),
        (eq, ":faction", "fac_kingdom_6"),
        (party_set_icon, ":cur_party", "icon_longship_hre"),
      (else_try),
        (eq, ":faction", "fac_kingdom_7"),
        (party_set_icon, ":cur_party", "icon_longship_hungary"),
      (else_try),
        (eq, ":faction", "fac_kingdom_8"),
        (party_set_icon, ":cur_party", "icon_longship_novgorod"),
      (else_try),
        (eq, ":faction", "fac_kingdom_9"),
        (party_set_icon, ":cur_party", "icon_longship_england"),
      (else_try),
        (eq, ":faction", "fac_kingdom_10"),
        (party_set_icon, ":cur_party", "icon_longship_france"),
      (else_try),
        (eq, ":faction", "fac_kingdom_11"),
        (party_set_icon, ":cur_party", "icon_longship_norway"),
      (else_try),
        (eq, ":faction", "fac_kingdom_12"),
        (party_set_icon, ":cur_party", "icon_longship_scotland"),
      (else_try),
        (eq, ":faction", "fac_kingdom_13"),
        (party_set_icon, ":cur_party", "icon_longship_ireland"),
      (else_try),
        (eq, ":faction", "fac_kingdom_14"),
        (party_set_icon, ":cur_party", "icon_longship_sweden"),
      (else_try),
        (eq, ":faction", "fac_kingdom_15"),
        (party_set_icon, ":cur_party", "icon_longship_galicia"),
      (else_try),
        (eq, ":faction", "fac_kingdom_16"),
        (party_set_icon, ":cur_party", "icon_longship_portugal"),
      (else_try),
        (eq, ":faction", "fac_kingdom_17"),
        (party_set_icon, ":cur_party", "icon_longship_aragon"),
      (else_try),
        (eq, ":faction", "fac_kingdom_18"),
        (party_set_icon, ":cur_party", "icon_longship_castile"),
      (else_try),
        (eq, ":faction", "fac_kingdom_19"),
        (party_set_icon, ":cur_party", "icon_longship_navarra"),
      (else_try),
        (eq, ":faction", "fac_kingdom_20"),
        (party_set_icon, ":cur_party", "icon_longship_granada"),
      (else_try),
        (eq, ":faction", "fac_papacy"),
        (party_set_icon, ":cur_party", "icon_longship_papal"),
      (else_try),
        (eq, ":faction", "fac_kingdom_22"),
        (party_set_icon, ":cur_party", "icon_longship_byzantine"),
      (else_try),
        (eq, ":faction", "fac_kingdom_23"),
        (party_set_icon, ":cur_party", "icon_longship_jerusalem"),
      (else_try),
        (eq, ":faction", "fac_kingdom_24"),
        (party_set_icon, ":cur_party", "icon_longship_sicily"),
      (else_try),
        (eq, ":faction", "fac_kingdom_25"),
        (party_set_icon, ":cur_party", "icon_longship_mamluke"),
      (else_try),
        (eq, ":faction", "fac_kingdom_26"),
        (party_set_icon, ":cur_party", "icon_longship_latin"),
      (else_try),
        (eq, ":faction", "fac_kingdom_27"),
        (party_set_icon, ":cur_party", "icon_longship_ilkhanate"),
      (else_try),
        (eq, ":faction", "fac_kingdom_28"),
        (party_set_icon, ":cur_party", "icon_longship_hafsid"),
      (else_try),
        (eq, ":faction", "fac_kingdom_29"),
        (party_set_icon, ":cur_party", "icon_longship_serbia"),
      (else_try),
        (eq, ":faction", "fac_kingdom_30"),
        (party_set_icon, ":cur_party", "icon_longship_bulgaria"),
      (else_try),
        (eq, ":faction", "fac_kingdom_31"),
        (party_set_icon, ":cur_party", "icon_longship_marinid"),
      (else_try),
        (eq, ":faction", "fac_outlaws"),
        (party_set_icon, ":cur_party", "icon_longship_pirate"),
      (else_try),
        (party_set_icon, ":cur_party", "icon_longship"),
      (try_end),
    (else_try),
      (eq, reg0, 0),
      (is_between, ":icon", "icon_longship", "icon_bandit_marker"),
      (neg|party_slot_eq, ":cur_party", party_slot_original_icon, 0),
      (party_get_slot, ":icon", ":cur_party", party_slot_original_icon),
      (party_set_icon, ":cur_party", ":icon"),
      # (eq, reg0, 0),
      # (party_get_icon, ":icon", ":cur_party"),
      # (is_between, ":icon", "icon_longship", "icon_bandit_marker"),
      # (try_begin),
        # (neq,reg0,1),
        # (party_get_template_id, ":cur_template", ":cur_party"),
        # (eq, ":cur_template", "pt_kingdom_hero_party"),
        # (party_set_icon, ":cur_party", "icon_flagbearer_a"),
      # (else_try),
       # (eq, ":cur_template", "pt_kingdom_caravan_party"),
       # (party_set_icon, ":cur_party", "icon_mule"),
      # (else_try),
        # (this_or_next | eq, ":cur_template", "pt_desert_bandits"),
        # (eq, ":cur_template", "pt_deserters"),
        # (party_set_icon, ":cur_party", "icon_vaegir_knight"),
      # (else_try),
        # (this_or_next|eq, ":cur_template", "pt_merc_party"),
        # (this_or_next|eq, ":cur_template", "pt_prisoner_train_party"),
        # (this_or_next|eq, ":cur_template", "pt_patrol_party"),
        # (this_or_next|eq, ":cur_template", "pt_ghibellines"),
        # (this_or_next|eq, ":cur_template", "pt_guelphs"),
        # (eq, ":cur_template", "pt_manhunters"),
        # (party_set_icon, ":cur_party", "icon_gray_knight"),      
      # (else_try),
        # (this_or_next|eq, ":cur_template", "pt_jihadist_raiders"),
        # (eq, ":cur_template", "pt_steppe_bandits"),
        # (party_set_icon, ":cur_party", "icon_khergit"),
      # (else_try),
        # (this_or_next|eq, ":cur_template", "pt_peasant_rebels_euro"),
        # (eq, ":cur_template", "pt_village_farmers"),
        # (party_set_icon, ":cur_party", "icon_peasant"),    
      # (else_try),
        # (eq, ":cur_template", "pt_cattle_herd"),
        # (party_set_icon, ":cur_party", "icon_cattle"),    
      # (else_try),
        # (this_or_next | eq, ":cur_template", "pt_crusaders"),
        # (this_or_next | eq, ":cur_template", "pt_crusader_raiders"),
        # (eq, ":cur_template", "pt_teutonic_raiders"),
        # (party_set_icon, ":cur_party", "icon_crusaders"),
      # (else_try),
        # (this_or_next | eq, ":cur_template", "pt_manhunters"),
        # (this_or_next | eq, ":cur_template", "pt_dplmc_recruiter"),
        # (eq, ":cur_template", "pt_merchant_caravan"),
        # (party_set_icon, ":cur_party", "icon_gray_knight"),
      # (else_try),
        # (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_patrol),
        # (party_slot_eq, ":cur_party", slot_party_type, spt_prisoner_train),      
        # (party_set_icon, ":cur_party", "icon_gray_knight"),      
      # (else_try),
        # (this_or_next|eq, ":cur_template", "pt_looters"),
        # (this_or_next|eq, ":cur_template", "pt_forest_bandits"),
        # (this_or_next|eq, ":cur_template", "pt_mountain_bandits"),
        # (this_or_next|eq, ":cur_template", "pt_taiga_bandits"),
        # (this_or_next|eq, ":cur_template", "pt_curonians"),
        # (this_or_next|eq, ":cur_template", "pt_prussians"),
        # (this_or_next|eq, ":cur_template", "pt_samogitians"),
        # (this_or_next|eq, ":cur_template", "pt_yotvingians"),
        # (this_or_next|eq, ":cur_template", "pt_welsh"),
        # (this_or_next|eq, ":cur_template", "pt_robber_knights"),
        # (this_or_next|eq, ":cur_template", "pt_troublesome_bandits"),
        # (this_or_next|eq, ":cur_template", "pt_bandits_awaiting_ransom"),
        # (eq, ":cur_template", "pt_sea_raiders"),
        # (party_set_icon, ":cur_party", "icon_axeman"),
      # (try_end),
    (try_end),
  (try_end),
]),

##diplomacy start
  # Appoint chamberlain
   (24 , 0, 24 * 7, 
   [],
   [
    (assign, ":has_fief", 0),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
      (eq, ":lord_troop_id", "trp_player"),
      (assign, ":has_fief", 1),
    (try_end),
    (eq, ":has_fief", 1),
    
    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (assign, reg0, "$g_player_chamberlain"),
      (display_message, "@{!}DEBUG : chamberlain: {reg0}"),
    (try_end),

    (assign, ":notification", 0),
    (try_begin),
      (eq, "$g_player_chamberlain", 0),
      (assign, ":notification", 1),
    (else_try),
      (neq, "$g_player_chamberlain", -1),
      (neq, "$g_player_chamberlain", "trp_dplmc_chamberlain"),
      (assign, ":notification", 1),
    (try_end),
    
    (try_begin),
      (eq, ":notification", 1),
      (call_script, "script_add_notification_menu", "mnu_dplmc_notification_appoint_chamberlain", 0, 0),
    (try_end),]
   ),
   
  # Appoint constable
   (24 , 0, 24 * 8, 
   [],
   [
    (assign, ":has_fief", 0),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
      (eq, ":lord_troop_id", "trp_player"),
      (assign, ":has_fief", 1),
    (try_end),
    (eq, ":has_fief", 1),
    
    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (assign, reg0, "$g_player_constable"),
      (display_message, "@{!}DEBUG : constable: {reg0}"),
    (try_end),

    (assign, ":notification", 0),
    (try_begin),
      (eq, "$g_player_constable", 0),
      (assign, ":notification", 1),
    (else_try),
      (neq, "$g_player_constable", -1),
      (neq, "$g_player_constable", "trp_dplmc_constable"),
      (assign, ":notification", 1),
    (try_end),
    
    (try_begin),
      (eq, ":notification", 1),
      (call_script, "script_add_notification_menu", "mnu_dplmc_notification_appoint_constable", 0, 0),
    (try_end),
    ]
   ),
   
  # Appoint chancellor
   (24 , 0, 24 * 9, 
   [],
   [
   (assign, ":has_fief", 0),
    (try_for_range, ":center_no", towns_begin, towns_end),
      (party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
      (eq, ":lord_troop_id", "trp_player"),
      (assign, ":has_fief", 1),
    (try_end),
    (eq, ":has_fief", 1),
    
    (try_begin), #debug
      (eq, "$cheat_mode", 1),
      (assign, reg0, "$g_player_chancellor"),
      (display_message, "@{!}DEBUG : chancellor: {reg0}"),
    (try_end),

    (assign, ":notification", 0),
    (try_begin),
      (eq, "$g_player_chancellor", 0),
      (assign, ":notification", 1),
    (else_try),
      (neq, "$g_player_chancellor", -1),
      (neq, "$g_player_chancellor", "trp_dplmc_chancellor"),
      (assign, ":notification", 1),
    (try_end),
    
    (try_begin),
      (eq, ":notification", 1),
      (call_script, "script_add_notification_menu", "mnu_dplmc_notification_appoint_chancellor", 0, 0),
    (try_end),
    ]
   ),
##diplomacy end
 

#crusader
(1.0, 24.0 * 4, 0, [
        #tom
        # (assign, "$crusade_target_faction", "fac_kingdom_33"),
        # (assign, "$crusader_state", 0),
        
        (eq, "$crusader_state", 0),
        (call_script, "script_diplomacy_start_war_between_kingdoms", "$crusader_faction", "$crusade_target_faction", 1),
        (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
          (neq, ":faction_no", "$crusader_faction"),
          (try_begin),
            (this_or_next|faction_slot_eq, ":faction_no", slot_faction_religion, religion_catholic),
            (faction_slot_eq, ":faction_no", slot_faction_religion, religion_orthodox),
            (set_relation, ":faction_no", "fac_crusade", 10),
          (else_try),
            (set_relation, ":faction_no", "fac_crusade", -50),
          (try_end),
        (try_end),
        
        (try_for_range, ":center",walled_centers_begin, walled_centers_end),
          (store_faction_of_party, ":faction_no", ":center"),
          (eq, "$crusader_faction", ":faction_no"), #player faction
          (assign, "$crusade_start", ":center"),
          (store_num_parties_of_template, ":num_parties", "pt_crusaders"),
          (lt, ":num_parties",1),
          (set_spawn_radius, 5),
          (spawn_around_party, "$crusade_start", "pt_crusaders"),
          (assign, ":party_id", reg0),        
          (assign, "$crusader_party_id", reg0),
          
          (party_set_ai_behavior, ":party_id", ai_bhvr_hold),
          (str_store_party_name_link, s1, ":center"),
          (str_store_faction_name_link, s2, "$crusade_target_faction"),
          (display_message, "@Crusaders are going to gather near {s1} the start their crusade against {s2}."),
          (assign, ":center", -1),
        (try_end),  
    ],
    [
        (try_begin), 
          #(store_num_parties_of_template, ":num_parties", "pt_crusaders"),
          #(eq, ":num_parties",1),
          #(set_spawn_radius, 5),
          (try_begin), 
            (lt, "$crusade_target", 0),  ######### NEW v2.6 - allows player to choose which fief to siege
            (try_for_range, ":center", walled_centers_begin, walled_centers_end),
              (store_faction_of_party, ":center_faction", ":center"),
              (eq, ":center_faction", "$crusade_target_faction"),
              (assign, "$crusade_target", ":center"),
            (try_end),
          (try_end),
          (str_store_faction_name_link, s1, "$crusade_target_faction"),
		  ############ New v1.9 - adds message with the target name
		  (str_store_party_name_link, s2, "$crusade_target"),
          (display_message, "@Crusade against {s1} have started! The target is {s2}."),
          ############
          #(spawn_around_party, "$crusade_start", "pt_crusaders"),
          #(assign, ":party_id", reg0),        
          #(assign, "$crusader_party_id", reg0),
          (assign, "$crusader_state", 1),
          (call_script, "script_party_set_ai_state", "$crusader_party_id", spai_besieging_center, "$crusade_target"),
        # (else_try),
          # (party_get_slot, ":ai_object", "$crusader_party_id", slot_party_ai_object),
          # (store_distance_to_party_from_party, ":distance", "$crusader_party_id", ":ai_object"),
          # (lt, ":distance", 3),
          # (neq, "$crusader_state", 1),
          # (store_current_hours, ":cur_hours"),
          # (party_set_slot, ":ai_object", slot_center_is_besieged_by, "$crusader_party_id"), #gali but kad party pasikeis, ie gaudys kokius pydarus?
          # (party_set_slot, ":ai_object", slot_center_siege_begin_hours, ":cur_hours"),
          # (party_set_ai_behavior, "$crusader_party_id", ai_bhvr_attack_party),
          # (party_set_ai_object, "$crusader_party_id", "p_town_21_1"),
          # (party_set_flags, "$crusader_party_id", pf_default_behavior, 1),
          # (party_set_slot, "$crusader_party_id", slot_party_ai_substate, 1),
          # (assign, "$crusader_state", 1),    
        (try_end),
    ]),
    
(1.0, 0, 0, [
        (eq, "$crusader_state", 0),
        (neq, "$crusader_party_id", -1),
    ],
    [
        
        (try_begin),
          (eq, "$crusader_faction", "fac_player_supporters_faction"),
          (party_get_slot, ":reinforcement_faction", "$crusade_start", slot_center_original_faction),
          (faction_get_slot, ":reinforcements_a", ":reinforcement_faction", slot_faction_reinforcements_a),
          (faction_get_slot, ":reinforcements_b", ":reinforcement_faction", slot_faction_reinforcements_b),
          (faction_get_slot, ":reinforcements_c", ":reinforcement_faction", slot_faction_reinforcements_b),
        (else_try),
          (faction_get_slot, ":reinforcements_a", "$crusader_faction", slot_faction_reinforcements_a),
          (faction_get_slot, ":reinforcements_b", "$crusader_faction", slot_faction_reinforcements_b),
          (faction_get_slot, ":reinforcements_c", "$crusader_faction", slot_faction_reinforcements_b),
        (try_end),  
        
        (store_random_in_range, ":random", 0, 4),
        (try_begin),
          (eq, ":random", 0),
          (party_add_template, "$crusader_party_id", ":reinforcements_a"),
        (else_try),
          (eq, ":random", 1),
          (party_add_template, "$crusader_party_id", ":reinforcements_b"),
        (else_try),
          (eq, ":random", 2),
          (party_add_template, "$crusader_party_id", ":reinforcements_c"),
        (else_try),
          (store_random_in_range, ":random", 0, 3),
          (try_begin),
            (eq, ":random", 0),
            (party_add_template, "$crusader_party_id", "pt_teutonic_reinforcements_c"),  
          (else_try),
            (eq, ":random", 1),
            (party_add_template, "$crusader_party_id", "pt_templar_reinforcements_c"),  
          (else_try),
            (party_add_template, "$crusader_party_id", "pt_hospitaller_reinforcements_c"),  
          (try_end),
          
        (try_end),
    ]),        

(1.0, 0, 0, [
        (eq, "$crusader_state", 1),
    ],
    [
        (try_begin),
          (store_num_parties_of_template, ":num_parties", "pt_crusaders"),
          (lt, ":num_parties",1),
          (assign, "$crusader_faction", -5),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusade_start", 0),
          (assign, "$crusade_target", -1),  ######## NEW v2.6 - shall fix the crusade attacking player bug
          (assign, "$crusade_target_faction", 0),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusader_state", -1), #-1 no crusade, 1 crusade started, 2 sieging, 3 storming
          (display_message, "@Crusaders have been defeated!"),
        (else_try),
          #(party_get_slot, ":ai_object", "$crusader_party_id", slot_party_ai_object),
          (store_distance_to_party_from_party, ":distance", "$crusader_party_id", "$crusade_target"),
          (lt, ":distance", 3),
          #(neq, "$crusader_state", 1),
          (store_current_hours, ":cur_hours"),
          (party_set_slot, "$crusade_target", slot_center_is_besieged_by, "$crusader_party_id"), #gali but kad party pasikeis, ie gaudys kokius pydarus?
          (party_set_slot, "$crusade_target", slot_center_siege_begin_hours, ":cur_hours"),
          (call_script, "script_update_faction_notes", "$crusade_target_faction"),
		  ############ New v1.9 - adds message with the target name
		  (str_store_party_name_link, s1, "$crusade_target"),
          (display_message, "@Crusaders have reached {s1}!"),
          ############
          # (party_set_ai_behavior, "$crusader_party_id", ai_bhvr_attack_party),
          # (party_set_ai_object, "$crusader_party_id", "p_town_21_1"),
          # (party_set_flags, "$crusader_party_id", pf_default_behavior, 1),
          # (party_set_slot, "$crusader_party_id", slot_party_ai_substate, 1),
          (assign, "$crusader_state", 2),      
        (else_try),
          (ge, ":distance", 3),
          (call_script, "script_party_set_ai_state", "$crusader_party_id", spai_besieging_center, "$crusade_target"),
        (try_end),  
    ]),    
    
(1.0, 24.0, 0, [
        (eq, "$crusader_state", 2),
    ],
    [
        (try_begin),
          (store_num_parties_of_template, ":num_parties", "pt_crusaders"),
          (lt, ":num_parties",1),
          (assign, "$crusader_faction", -5),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusade_start", 0),
          (assign, "$crusade_target", -1), ######## NEW v2.6 - shall fix the crusade attacking player bug
          (assign, "$crusade_target_faction", 0),
          (assign, "$crusader_state", -1), #-1 no crusade, 1 crusade started, 2 sieging, 3 storming
          (display_message, "@Crusaders have been defeated!"),
        (else_try),
          #(party_get_slot, ":ai_object", "$crusader_party_id", slot_party_ai_object),
          (store_distance_to_party_from_party, ":distance", "$crusader_party_id", "$crusade_target"),
          (lt, ":distance", 5),
          (call_script, "script_party_set_ai_state", "$crusader_party_id", spai_besieging_center, "$crusade_target"),
          (party_set_ai_behavior, "$crusader_party_id", ai_bhvr_attack_party),
          (party_set_ai_object, "$crusader_party_id", "$crusade_target"),
          (party_set_flags, "$crusader_party_id", pf_default_behavior, 1),
          (party_set_slot, "$crusader_party_id", slot_party_ai_substate, 1),
		  ############ New v1.9 - adds message with the target name
		  (str_store_party_name_link, s1, "$crusade_target"),
          (display_message, "@Crusaders have besieged {s1}!"),
		  ############
          (assign, "$crusader_state", 3),    
        (else_try),
          (assign, "$crusader_state", 1),    
          (party_set_slot, "$crusade_target", slot_center_is_besieged_by, "$crusader_party_id"),
          (party_get_slot, ":sieged_by", "$crusade_target",slot_center_is_besieged_by),
          (eq, ":sieged_by", "$crusader_party_id"),
          (party_set_slot, "$crusade_target", slot_center_is_besieged_by, -1),
        (try_end),  
    ]),    
    
(1.0, 0, 0, [
        (eq, "$crusader_state", 3),
    ],
    [
        (try_begin),
          (store_num_parties_of_template, ":num_parties", "pt_crusaders"),
          (lt, ":num_parties",1),
          (assign, "$crusader_faction", -5),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusade_start", 0),
          (assign, "$crusade_target", -1), ######## NEW v2.6 - shall fix the crusade attacking player bug
          (assign, "$crusade_target_faction", 0),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusader_state", -1), #-1 no crusade, 1 crusade started, 2 sieging, 3 storming
          (display_message, "@Crusaders have been defeated!"),
        (else_try),
          (assign, ":center_gaved", 0),
          (try_for_range, ":center",walled_centers_begin, walled_centers_end),
            (store_faction_of_party, ":faction", ":center"),
            (eq, ":faction", "fac_crusade"),
            (try_begin),
              (eq, ":center", "p_town_21_1"), #rome
              (call_script, "script_give_center_to_faction_aux", "p_town_21_1", "fac_papacy"),
              (faction_set_slot, "fac_papacy", slot_faction_state, sfs_active),
              (faction_set_slot, "fac_papacy",  slot_faction_leader, "trp_pope"),
              (call_script, "script_give_center_to_lord", "p_town_21_1",  "trp_pope", 1),
              (party_set_slot, "p_town_21_1",slot_crusade,0),
              (assign, ":center_gaved", 1),
            (else_try),
              (eq, ":center", "p_town_25_5"), #jerusalem
              (call_script, "script_give_center_to_faction_aux", "p_town_25_5", "fac_kingdom_23"),
              (faction_set_slot, "fac_kingdom_23", slot_faction_state, sfs_active),
              (faction_set_slot, "fac_kingdom_23",  slot_faction_leader, "trp_kingdom_23_lord"),
              (call_script, "script_give_center_to_lord", "p_town_25_5",  "trp_kingdom_23_lord", 1),
              (party_set_slot, "p_town_25_5",slot_crusade,0),
              (assign, ":center_gaved", 1),
            (else_try),
              (call_script, "script_give_center_to_faction_aux", ":center", "$crusader_faction"),
              (try_begin),
                (eq, "$players_kingdom", "$crusader_faction"),
                (call_script, "script_give_center_to_lord", ":center",  "trp_player", 1),
              (else_try),
                (call_script, "script_cf_get_random_lord_except_king_with_faction", "$crusader_faction"),
                (gt, reg0, -1),
                (call_script, "script_give_center_to_lord", ":center",  reg0, 1),
              (try_end),
              (assign, ":center_gaved", 1),
            (try_end),            
          (try_end),
          (eq, ":center_gaved", 1),
          (party_leave_cur_battle, "$crusader_party_id"),
          (remove_party, "$crusader_party_id"),
		  ############ New v1.9 - adds message with the target name
		  (str_store_party_name_link, s1, "$crusade_target"),
          (display_message, "@Crusade ended successfully! {s1} was captured."),
          ############
          (assign, "$crusader_faction", -5),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusade_start", 0),
          (assign, "$crusade_target", -1), ######## NEW v2.6 - shall fix the crusade attacking player bug
          (assign, "$crusade_target_faction", 0),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusader_state", -1), #-1 no crusade, 1 crusade started, 2 sieging, 3 storming

      (else_try),
        # (try_end),
        # (try_begin),
          (neq, "$crusader_party_id", -1),
          (store_faction_of_party, ":faction", "$crusade_target"),
          (neq, ":faction", "$crusade_target_faction"),
          (display_message, "@Crusaders disperse, because someone else conquered the center."),
          (party_leave_cur_battle, "$crusader_party_id"),
          (remove_party, "$crusader_party_id"),
          (assign, "$crusader_faction", -5),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusade_start", 0),
          (assign, "$crusade_target", -1),  ######## NEW v2.6 - shall fix the crusade attacking player bug
          (assign, "$crusade_target_faction", 0),
          (assign, "$crusader_party_id", -1),
          (assign, "$crusader_state", -1), #-1 no crusade, 1 crusade started, 2 sieging, 3 storming
         (else_try),
            (call_script, "script_party_set_ai_state", "$crusader_party_id", spai_besieging_center, "$crusade_target"),
        (try_end),  
    ]),        
    
    #auto crusade
(24.0, 0.0, 0, [
        (eq, "$crusader_state", -1),
        (store_random_in_range, reg0, 0, 400),
        
        #(assign, reg0, 0), #temp
        # (eq, reg0, 0),
        (lt, reg0, "$g_misc_crusade_daily_chance"),  ######## NEW v2.1 
    ],
    [
        #crusade from
        (try_for_range, ":faction_no", 0, 40),
          (troop_set_slot, "trp_temp_lord", ":faction_no", -1), #catholic factions
        (try_end),
        (assign, reg0, 0),
        (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
          (neq, ":faction_no", "fac_player_supporters_faction"),
          (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
          (faction_slot_eq, ":faction_no", slot_faction_religion, religion_catholic),
          (troop_set_slot, "trp_temp_lord",reg0, ":faction_no"), #catholic factions
          (val_add, reg0, 1),
        (try_end),
        (gt, reg0, 0),
        #(val_add, reg0, 1),
        (store_random_in_range, ":i", 0, reg0),
        (troop_get_slot, ":faction_no", "trp_temp_lord", ":i"), 
        (assign, "$crusader_state", 0),
        (assign, "$crusader_faction", ":faction_no"),
        
        #crusade at
        (try_for_range, ":faction_no", 0, 40),
          (troop_set_slot, "trp_temp_lord", ":faction_no", -1),#muslim factions
        (try_end),
        (assign, reg0, 0),
        (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
          (neg|faction_slot_eq, ":faction_no", slot_faction_religion, religion_catholic), 
          (neg|faction_slot_eq, ":faction_no", slot_faction_religion, religion_orthodox),
          (troop_set_slot, "trp_temp_lord",reg0, ":faction_no"), #muslim factions
          (val_add, reg0, 1),
        (try_end),
        (gt, reg0, 0),
        #(val_add, reg0, 1),
        (store_random_in_range, ":i", 0, reg0),
        (troop_get_slot, ":faction_no", "trp_temp_lord", ":i"), 
        (assign, "$crusade_target_faction", ":faction_no"),
    ]),        
    
    ###camp bonuses
    (3.0, 0.0, 12, 
    [
      # (eq, 0, 1),
      (this_or_next|eq, "$g_camp_mode", 1),
      (eq, "$g_town_visit_after_rest", 1),  ############# NEW v2.0 - works in fiefs too
      (is_currently_night),
    ],
    [
	############### NEW v1.9
        (display_message, "@Resting at night. Morale increased by 5.", 0x50FF50),
        (party_get_morale, ":morale", "p_main_party"),
        (val_add, ":morale", 5),
        (party_set_morale, "p_main_party", ":morale" ),
    ]),        


    ###captains following around
    (1, 0.0, 0, 
    [
      (store_num_parties_of_template, ":num_parties", "pt_merc_party"),
      (ge, ":num_parties", 1),
    ],
    [
        #(assign, ":last_party", -1),
        #(assign, ":total_wage", 0),
        (try_for_parties, ":party"),
          (party_get_template_id, ":template", ":party"),
          (eq, ":template", "pt_merc_party"),
          (party_set_faction, ":party", "$players_kingdom"),
          #do ai
          (party_get_slot, ":state", ":party", slot_party_ai_state),
          (party_get_slot, ":object", ":party", slot_party_ai_object),
          (try_begin),
            (eq, ":state", ai_bhvr_patrol_location),
            (store_distance_to_party_from_party, ":distance", ":party", ":object"),
            (try_begin),
              (gt, ":distance", 10),
              (party_set_ai_behavior, ":party", ai_bhvr_travel_to_point),
              (party_get_position, pos5, ":object"),
              (party_set_ai_target_position, ":party", pos5),
            (else_try),  
              (party_set_ai_behavior, ":party", ai_bhvr_patrol_location),
              (party_set_ai_object, ":party", ":object"),
              (party_set_ai_patrol_radius, ":party", 5),
            (try_end),  
          (else_try), #follow player otherwise    
            (eq, ":object", "p_main_party"),
            (party_set_ai_behavior, ":party", ai_bhvr_escort_party),
            (party_set_ai_object, ":party", "p_main_party"),
          (try_end),
          #remove it if too small
          (store_party_size_wo_prisoners, ":size", ":party"),
          (try_begin),
            (le, ":size", 10),
            (remove_party, ":party"),
          (try_end),
        (try_end),
    ]),
    
    ###captains pay each week
    (24.0*7, 0.0, 0, 
    [
      (store_num_parties_of_template, ":num_parties", "pt_merc_party"),
      (ge, ":num_parties", 1),
    ],
    [      
        (assign, ":last_party", -1),
        (assign, ":total_wage", 0),
        (try_for_parties, ":party"),
          (party_get_template_id, ":template", ":party"),
          (eq, ":template", "pt_merc_party"),
          #(party_set_faction, ":party", "$players_kingdom"),
          #PAY MONEY MONEY MONEY MONEY
          (party_get_num_companion_stacks, ":num_stacks", ":party"),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
            (party_stack_get_size, ":stack_size", ":party", ":i_stack"),
            (call_script, "script_game_get_troop_wage", ":stack_troop", 0),
            (val_mul, reg0, ":stack_size"),
            (val_add, ":total_wage", reg0),
          (try_end),
          (assign, ":last_party", ":party"),
        (try_end),#end cycle
        
        (store_troop_gold, ":gold", "trp_player"),
        #enough gold?
        (assign, ":rebel", 0),
        (try_begin),
          (lt, ":gold", ":total_wage"),
          (assign, ":rebel", 1),
          (assign, ":total_wage", ":gold"),
          (display_message, "@you do not have enough gold to pay your forces!"),
        (try_end),
        #lets turn to bandits
        (try_begin),
          (eq, ":rebel", 1),
          (neq, ":last_party", -1),
          (store_random_in_range, ":random", 0, 100),
          (lt, ":random", 30),
          # (party_set_faction, ":last_party", "fac_deserters"),
          # (party_set_ai_behavior, ":party", ai_bhvr_attack_party),
          # (party_set_ai_object, ":party", "p_main_party"),
          (set_spawn_radius, 1),
          (spawn_around_party, ":last_party", "pt_deserters"),
          (assign, ":new_party", reg0),
          
          (party_clear, ":new_party"),
          (party_get_num_companion_stacks, ":num_stacks", ":party"),
          (try_for_range, ":i_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":last_party", ":i_stack"),
            (party_stack_get_size, ":stack_size", ":last_party", ":i_stack"),
            (party_add_members, ":new_party", ":stack_troop", ":stack_size"),
            #(party_remove_members, ":last_party", ":stack_troop", ":stack_size"),
          (try_end),
          (remove_party, ":last_party"),
          (party_set_ai_behavior, ":new_party", ai_bhvr_attack_party),
          (party_set_ai_object, ":new_party", "p_main_party"),
          (display_message, "@One of your armies have deserted you!"), #TODO THIS
        (try_end),
        (troop_remove_gold, "trp_player", ":total_wage"),
    ]),    

    ###MONGOL CAMPS
    #spawning, reinforcement, utility
    (24.0*7, 0.0, 0, 
    #(6, 0.0, 0, 
    [
    ],
    [    
    #(display_message, "@utility trigger"),
        #remove the bounds of destroyed/inactive parties of mongolian camps. Then spawn new ones(maybe)
        (try_for_range, ":town", centers_begin, centers_end),
          (party_get_slot, ":camp", ":town", slot_mongol_camp),
          (this_or_next|eq, ":camp", 0),
          (neg|party_is_active, ":camp"),
          (party_set_slot, ":town",slot_mongol_camp,-1),  
          
          (store_faction_of_party, ":faction", ":town"),
          (this_or_next|eq, ":faction", "fac_kingdom_3"),
          (eq, ":faction", "fac_kingdom_27"),
          #(str_store_party_name,s0, ":town"),
          #TODO MONGOLIANS INVITED INTO TOWN
          #(party_get_slot, ":camp", ":town",slot_mongol_camp),
          #(le, ":camp", 0),
          #(store_random_in_range, ":random", 1, 101),
         # (ge, ":random", 50),
          (set_spawn_radius, 5),
          (spawn_around_party, ":town", "pt_mongolian_camp"),
          (assign, ":party_id", reg0),
          (party_set_ai_behavior, ":party_id", ai_bhvr_patrol_location),
          (party_set_ai_object, ":party_id", ":town"),
          (party_set_slot, ":party_id", slot_party_ai_object, ":town"),
          (party_set_ai_patrol_radius, ":party_id", 10),
          
          (party_set_slot, ":party_id",slot_mongol_town, ":town"),
          (party_set_slot, ":town",slot_mongol_camp, ":party_id"),
          (party_set_faction, ":party_id", ":faction"),
          (party_set_slot, ":party_id", slot_castle_exterior, "scn_village_mongol"),
          (party_set_slot, ":party_id", slot_feudal_lances, 1),#one lance!
          (party_set_slot, ":party_id", slot_center_culture, "fac_culture_mongol"),
          (party_set_slot, ":party_id", slot_mongol_camp_status, status_stationed),
          (party_set_slot, ":party_id", slot_town_prosperity, 50),
          (party_set_slot, ":party_id", slot_party_type, spt_mongol_party),
          (party_set_icon, ":party_id", "icon_camp"),
        (try_end),
        
        #Sarai always spawns one, even if sarai isn't mongolian
        (try_begin),
          (assign, ":town", "p_town_3_1"),
          (party_get_slot, ":camp", ":town",slot_mongol_camp),
          (le, ":camp", 0),
          
          (store_faction_of_party, ":faction", ":town"),
          #(store_random_in_range, ":random", 1, 101),
          #(ge, ":random", 30),
          (set_spawn_radius, 5),
          (spawn_around_party, ":town", "pt_mongolian_camp"),
          (assign, ":party_id", reg0),
          (party_set_ai_behavior, ":party_id", ai_bhvr_patrol_location),
          (party_set_ai_object, ":party_id", ":town"),
          (party_set_slot, ":party_id", slot_party_ai_object, ":town"),
          (party_set_ai_patrol_radius, ":party_id", 10),
          
          (party_set_slot, ":party_id",slot_mongol_town, ":town"),
          (party_set_slot, ":town",slot_mongol_camp, ":party_id"),
          (party_set_faction, ":party_id", ":faction"),
          (party_set_slot, ":party_id",slot_castle_exterior, "scn_village_mongol"),
          (party_set_slot, ":party_id", slot_feudal_lances, 1),#one lance!
          (party_set_slot, ":party_id", slot_center_culture, "fac_culture_mongol"),
          (party_set_slot, ":party_id",slot_mongol_camp_status, status_stationed),
          (party_set_slot, ":party_id", slot_town_prosperity, 50),
          (party_set_slot, ":party_id", slot_party_type, spt_mongol_party),
          (party_set_icon, ":party_id", "icon_camp"),
        (try_end),    
    ]),
    
    #relocation and reinforcement trigger
    (24.0*2, 0.0, 0, 
    #(3, 0.0, 0, 
    [
        (store_num_parties_of_template, ":amount", "pt_mongolian_camp"),
        (gt, ":amount", 0),
    ],
    [    
    #(display_message, "@start relocation trigger"),
        (try_for_parties, ":camp"),
          (party_get_template_id, ":template", ":camp"),
          (eq, ":template", "pt_mongolian_camp"),
          (party_is_active, ":camp"),
          (party_get_slot, ":camp_status", ":camp", slot_mongol_camp_status),
          
          ##RELOCATION
          (try_begin), #start relocation
            (eq, ":camp_status", status_stationed),
            (store_random_in_range, ":random", 0, 100),
            (le, ":random", 50),
            (party_set_slot, ":camp",slot_mongol_camp_status, status_moving),
            (party_set_icon, ":camp", "icon_khergit"),
          
            (party_get_slot, ":town", ":camp", slot_mongol_town),
            (party_set_ai_behavior, ":camp", ai_bhvr_patrol_location),
            (party_set_ai_object, ":camp", ":town"),
            (party_set_slot, ":camp", slot_party_ai_object, ":town"),
            (party_set_ai_patrol_radius, ":camp", 10),
          (else_try), #end relocation
            #(eq, ":camp_status", status_moving),
            (store_faction_of_party, ":camp_faction", ":camp"),
            (party_get_slot, ":town", ":camp", slot_mongol_town),
            (store_faction_of_party, ":town_faction", ":town"),
            (eq, ":town_faction", ":camp_faction"), #if town and camp factions are diffrent, camp continues to raid around town
            (party_set_slot, ":camp",slot_mongol_camp_status, status_stationed),
            (party_set_icon, ":camp", "icon_camp"),
          (try_end),
          ##RELOCATION END
          ##REINFORCEMENT START Limit - 100 men.
          (try_begin),
            (store_party_size_wo_prisoners, ":party_size", ":camp"),
            (le, ":party_size", 100), ###PARTY SIZE limit - 100
            (store_random_in_range, ":random", 1, 101),
            (try_begin),
              (le, ":random", 25),
              (assign, ":reinf", "pt_kingdom_mongol_reinforcements_c"),
            (else_try),
              (ge, ":random", 75),
              (assign, ":reinf", "pt_kingdom_mongol_reinforcements_b"),
            (else_try),
              (assign, ":reinf", "pt_kingdom_mongol_reinforcements_a"),
            (try_end),
            (party_add_template, ":camp", ":reinf"),
            #lances
            (party_get_slot, ":manpower", ":camp", slot_feudal_lances),
            (lt, ":manpower", 6),
            (val_add, ":manpower", 1),
            (party_set_slot, ":camp", slot_feudal_lances, ":manpower"),
          (try_end),
          ##REINFORCEMENT END
        (try_end),
    ]),
    ###MONGOL CAMPS END
    
    
############### NEW v2.0
    (6.0, 0.0, 24, 
    [
      # (eq, 0, 1),
      (eq, "$g_town_visit_after_rest", 1),
      # (is_currently_night),
    ],
    [
      (display_message, "@Resting at a walled fief. Morale increased by 5.", 0x50FF50),
      (party_get_morale, ":morale", "p_main_party"),
      (val_add, ":morale", 5),
      (party_set_morale, "p_main_party", ":morale" ),
    ]),        
##############################


################# NEW v2.1 - Apply effects at game start
  (0.05, 0, ti_once,
   [
      (map_free),
    ],
   [
    (try_begin),
      (faction_get_slot, ":cur_faction_culture", "$players_kingdom", slot_faction_culture),
      (try_begin),
        (eq, ":cur_faction_culture", "fac_culture_finnish"),
          (assign, "$g_player_know_culture_finnish", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_mazovian"),
          (assign, "$g_player_know_culture_mazovian", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_serbian"),
          (assign, "$g_player_know_culture_serbian", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_welsh"),
          (assign, "$g_player_know_culture_welsh", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_teutonic"),
          (assign, "$g_player_know_culture_teutonic", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_balkan"),
          (assign, "$g_player_know_culture_balkan", 1),
          
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_rus"),
          (assign, "$g_player_know_culture_rus", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_nordic"),
          (assign, "$g_player_know_culture_nordic", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_baltic"),
          (assign, "$g_player_know_culture_baltic", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_marinid"),
          (assign, "$g_player_know_culture_marinid", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_mamluke"),
          (assign, "$g_player_know_culture_mamluke", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_byzantium"),
          (assign, "$g_player_know_culture_byzantium", 1),
          
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_iberian"),
          (assign, "$g_player_know_culture_iberian", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_italian"),
          (assign, "$g_player_know_culture_italian", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_andalus"),
          (assign, "$g_player_know_culture_andalus", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_gaelic"),
          (assign, "$g_player_know_culture_gaelic", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_anatolian_christian"),
          (assign, "$g_player_know_culture_anatolian_christian", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_anatolian"),
          (assign, "$g_player_know_culture_anatolian", 1),
          
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_western"),
          (assign, "$g_player_know_culture_western", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_mongol"),
          (assign, "$g_player_know_culture_mongol", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_templar"),
          (assign, "$g_player_know_culture_templar", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_hospitaller"),
          (assign, "$g_player_know_culture_hospitaller", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_antioch"),
          (assign, "$g_player_know_culture_antiochian", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_tripoli"),
          (assign, "$g_player_know_culture_tripoli", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_ibelin"),
          (assign, "$g_player_know_culture_ibelin", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_jerusalem"),
          (assign, "$g_player_know_culture_jerusalem", 1),
      (else_try),
        (eq, ":cur_faction_culture", "fac_culture_player"),
          (assign, "$g_player_know_culture_player", 1),      
      (try_end),
    (try_end),
	
    (try_begin),    
      (call_script, "script_assign_lord_face_type"),    ###### assign face types to lords  
	(try_end),
	
    ############ This will set the religion of faction that have leaders of a different religion
    (faction_set_slot, "fac_kingdom_3", slot_faction_religion, religion_muslim),  ### Golden Horde - Berke Khan
    (faction_set_slot, "fac_kingdom_27", slot_faction_religion, religion_pagan_mongol), ### Ilkhanate - Hulagu Khan
    (faction_set_slot, "fac_kingdom_26", slot_faction_religion, religion_catholic), ###### Latin Empire - Catholic

   ]
),
##############################




############ NEW v1.0 -  [OSP] Advanced Soldier Management in Exchange Screens 
# (0,0, ti_on_switch_to_map, [],
  # [
  # (troop_set_slot, "trp_globals_troop", slot_adv_transfer_mode, 0),
  # ]
# ),
#############################


##############################
]#############################
##############################
# modmerger_start version=201 type=2
try:
    component_name = "triggers"
    var_set = { "triggers" : triggers }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end