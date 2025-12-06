import math

from planner import plan_story


def test_story_scene_planner_basic_structure():
    script = """
    [SCENE 1]
    Mata Amrit: Ardas karie ate gurdwara ch langar seva kariye.
    Kid Harjit: Ji Maa, main tayar haan.

    [SCENE 2]
    Coach Singh: Playground te cricket practice shuru kariye.
    Player Simran: Main run-up ready kar rahi haan.
    """

    plan = plan_story(script, story_id="demo_story")

    assert plan["story_id"] == "demo_story"
    assert plan["language"] in {"pa", "en"}
    assert len(plan["scenes"]) == 2

    scene1 = plan["scenes"][0]
    assert scene1["location"]["tag"] == "gurdwara"
    roles_scene1 = {character["role"] for character in scene1["characters"]}
    assert roles_scene1  # at least one character detected
    assert "mother" in roles_scene1 or "kid" in roles_scene1
    assert scene1["narration"][0]["speaker"].lower().startswith("mata")
    assert scene1["duration_hint"] >= 6.0

    scene2 = plan["scenes"][1]
    assert scene2["location"]["tag"] == "sports_ground"
    actions_scene2 = {character.get("action") for character in scene2["characters"]}
    assert actions_scene2.intersection({"cricket_bat", "run"})
    assert math.isclose(float(scene2["duration_hint"]), round(float(scene2["duration_hint"]), 1))
