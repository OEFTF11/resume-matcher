from resume_matcher.score import score_match


def test_score_match_basic():
    resume = {"python", "sql", "flask", "docker"}
    jd = {"python", "sql", "kubernetes"}

    result = score_match(resume, jd, fuzzy_threshold=100)

    assert result.score == 67
    assert "python" in result.matched
    assert "sql" in result.matched
    assert "kubernetes" in result.missing
