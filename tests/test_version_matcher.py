"""Unit tests for version_matcher module."""

import unittest
from src.version_matcher import VersionMatcher


class TestVersionMatcher(unittest.TestCase):
    """Test cases for VersionMatcher class."""
    
    def test_normalize_version_with_tuxcare_suffix(self):
        """Test version normalization with .tuxcare suffix."""
        self.assertEqual(
            VersionMatcher.normalize_version("30.1-jre.tuxcare"),
            "30.1-jre"
        )
        self.assertEqual(
            VersionMatcher.normalize_version("2.7.18.tuxcare.3"),
            "2.7.18"
        )
        self.assertEqual(
            VersionMatcher.normalize_version("1.0.0.tuxcare"),
            "1.0.0"
        )
    
    def test_normalize_version_without_suffix(self):
        """Test version normalization without suffix."""
        self.assertEqual(
            VersionMatcher.normalize_version("30.1-jre"),
            "30.1-jre"
        )
        self.assertEqual(
            VersionMatcher.normalize_version("1.0.0"),
            "1.0.0"
        )
    
    def test_normalize_version_empty(self):
        """Test version normalization with empty string."""
        self.assertEqual(VersionMatcher.normalize_version(""), "")
    
    def test_parse_version_valid(self):
        """Test parsing valid version strings."""
        version = VersionMatcher.parse_version("1.0.0")
        self.assertIsNotNone(version)
        
        version = VersionMatcher.parse_version("30.1-jre")
        self.assertIsNotNone(version)
    
    def test_parse_version_with_tuxcare(self):
        """Test parsing versions with TuxCare suffix."""
        version = VersionMatcher.parse_version("30.1-jre.tuxcare")
        self.assertIsNotNone(version)
    
    def test_parse_version_invalid(self):
        """Test parsing invalid version strings."""
        version = VersionMatcher.parse_version("")
        self.assertIsNone(version)
    
    def test_parse_range_spec_single(self):
        """Test parsing single constraint."""
        ranges = VersionMatcher.parse_range_spec(">= 1.0.0")
        self.assertEqual(ranges, [(">=", "1.0.0")])
        
        ranges = VersionMatcher.parse_range_spec("< 2.0.0")
        self.assertEqual(ranges, [("<", "2.0.0")])
    
    def test_parse_range_spec_multiple(self):
        """Test parsing multiple constraints."""
        ranges = VersionMatcher.parse_range_spec(">= 1.0.0, < 2.0.0")
        self.assertEqual(ranges, [(">=", "1.0.0"), ("<", "2.0.0")])
    
    def test_parse_range_spec_equal(self):
        """Test parsing equality constraint."""
        ranges = VersionMatcher.parse_range_spec("= 1.5.0")
        self.assertEqual(ranges, [("=", "1.5.0")])
    
    def test_parse_range_spec_empty(self):
        """Test parsing empty range spec."""
        ranges = VersionMatcher.parse_range_spec("")
        self.assertEqual(ranges, [])
    
    def test_version_satisfies_constraint_gte(self):
        """Test >= constraint."""
        from packaging import version
        v = version.parse("2.0.0")
        constraint = version.parse("1.0.0")
        
        result = VersionMatcher.version_satisfies_constraint(v, ">=", constraint)
        self.assertTrue(result)
        
        v = version.parse("0.9.0")
        result = VersionMatcher.version_satisfies_constraint(v, ">=", constraint)
        self.assertFalse(result)
    
    def test_version_satisfies_constraint_lt(self):
        """Test < constraint."""
        from packaging import version
        v = version.parse("1.0.0")
        constraint = version.parse("2.0.0")
        
        result = VersionMatcher.version_satisfies_constraint(v, "<", constraint)
        self.assertTrue(result)
        
        v = version.parse("2.5.0")
        result = VersionMatcher.version_satisfies_constraint(v, "<", constraint)
        self.assertFalse(result)
    
    def test_version_satisfies_constraint_equal(self):
        """Test = constraint."""
        from packaging import version
        v = version.parse("1.5.0")
        constraint = version.parse("1.5.0")
        
        result = VersionMatcher.version_satisfies_constraint(v, "=", constraint)
        self.assertTrue(result)
        
        v = version.parse("1.5.1")
        result = VersionMatcher.version_satisfies_constraint(v, "=", constraint)
        self.assertFalse(result)
    
    def test_version_in_range_simple(self):
        """Test version in simple range."""
        result = VersionMatcher.version_in_range("1.5.0", ">= 1.0.0, < 2.0.0")
        self.assertTrue(result)
        
        result = VersionMatcher.version_in_range("2.5.0", ">= 1.0.0, < 2.0.0")
        self.assertFalse(result)
    
    def test_version_in_range_with_tuxcare(self):
        """Test version in range with TuxCare suffix."""
        # 30.1 should be in range >= 25.0, < 32.0
        result = VersionMatcher.version_in_range(
            "30.1-jre.tuxcare",
            ">= 25.0, < 32.0"
        )
        self.assertTrue(result)
        
        # 33.0 should not be in range >= 25.0, < 32.0
        result = VersionMatcher.version_in_range(
            "33.0.tuxcare",
            ">= 25.0, < 32.0"
        )
        self.assertFalse(result)
    
    def test_version_in_range_edge_cases(self):
        """Test edge cases for version in range."""
        # Empty version
        result = VersionMatcher.version_in_range("", ">= 1.0.0")
        self.assertFalse(result)
        
        # Empty range
        result = VersionMatcher.version_in_range("1.0.0", "")
        self.assertFalse(result)
    
    def test_matches_alert_same_package(self):
        """Test matching with same package name."""
        result = VersionMatcher.matches_alert(
            vex_version="30.1-jre.tuxcare",
            alert_version_range=">= 25.0, < 32.0",
            vex_package="com.google.guava:guava",
            alert_package="com.google.guava:guava"
        )
        self.assertTrue(result)
    
    def test_matches_alert_different_package(self):
        """Test matching with different package names."""
        result = VersionMatcher.matches_alert(
            vex_version="30.1-jre.tuxcare",
            alert_version_range=">= 25.0, < 32.0",
            vex_package="com.google.guava:guava",
            alert_package="org.apache.commons:commons-lang3"
        )
        self.assertFalse(result)
    
    def test_matches_alert_version_outside_range(self):
        """Test matching with version outside range."""
        result = VersionMatcher.matches_alert(
            vex_version="35.0.tuxcare",
            alert_version_range=">= 25.0, < 32.0",
            vex_package="com.google.guava:guava",
            alert_package="com.google.guava:guava"
        )
        self.assertFalse(result)
    
    def test_extract_base_version(self):
        """Test extracting base version."""
        self.assertEqual(
            VersionMatcher.extract_base_version("30.1-jre.tuxcare"),
            "30.1-jre"
        )
        self.assertEqual(
            VersionMatcher.extract_base_version("1.0.0.tuxcare.5"),
            "1.0.0"
        )
        self.assertEqual(
            VersionMatcher.extract_base_version("1.0.0"),
            "1.0.0"
        )
    
    def test_extract_exact_version_simple(self):
        """Test extracting exact version from simple string."""
        self.assertEqual(
            VersionMatcher.extract_exact_version("1.2.17"),
            "1.2.17"
        )
        self.assertEqual(
            VersionMatcher.extract_exact_version("= 1.2.17"),
            "1.2.17"
        )
        self.assertEqual(
            VersionMatcher.extract_exact_version("== 1.2.17"),
            "1.2.17"
        )
    
    def test_extract_exact_version_maven(self):
        """Test extracting exact version from Maven format."""
        # Exact version in Maven [1.2.17]
        self.assertEqual(
            VersionMatcher.extract_exact_version("[1.2.17]"),
            "1.2.17"
        )
        # Maven range [1.2.17,) - brackets only removed if both present
        # This returns the bracket because it doesn't end with ]
        self.assertEqual(
            VersionMatcher.extract_exact_version("[1.2.17,)"),
            "[1.2.17,)"
        )
    
    def test_extract_exact_version_operators(self):
        """Test extracting version with various operators."""
        self.assertEqual(
            VersionMatcher.extract_exact_version(">= 1.2.17"),
            "1.2.17"
        )
        self.assertEqual(
            VersionMatcher.extract_exact_version("^1.2.17"),
            "1.2.17"
        )
        self.assertEqual(
            VersionMatcher.extract_exact_version("~1.2.17"),
            "1.2.17"
        )
    
    def test_extract_exact_version_empty(self):
        """Test extracting from empty string."""
        self.assertIsNone(VersionMatcher.extract_exact_version(""))
        self.assertIsNone(VersionMatcher.extract_exact_version(None))
    
    def test_versions_match_exact(self):
        """Test exact version matching."""
        # Repo has TuxCare version, VEX has same TuxCare version -> MATCH
        self.assertTrue(
            VersionMatcher.versions_match("1.2.17.tuxcare.1", "1.2.17.tuxcare.1")
        )
        
        # With equals sign
        self.assertTrue(
            VersionMatcher.versions_match("= 1.2.17.tuxcare.1", "1.2.17.tuxcare.1")
        )
        
        # Maven bracket format
        self.assertTrue(
            VersionMatcher.versions_match("[1.2.17.tuxcare.1]", "1.2.17.tuxcare.1")
        )
    
    def test_versions_match_mismatch(self):
        """Test version mismatch scenarios."""
        # Vanilla version vs TuxCare version should NOT match
        self.assertFalse(
            VersionMatcher.versions_match("1.2.17", "1.2.17.tuxcare.1")
        )
        
        # Different base versions should NOT match
        self.assertFalse(
            VersionMatcher.versions_match("1.2.16.tuxcare.1", "1.2.17.tuxcare.1")
        )
        
        self.assertFalse(
            VersionMatcher.versions_match("1.2.18.tuxcare.1", "1.2.17.tuxcare.1")
        )
        
        # Vanilla older version should not match
        self.assertFalse(
            VersionMatcher.versions_match("1.2.0", "1.2.17.tuxcare.1")
        )
    
    def test_versions_match_both_tuxcare(self):
        """Test when both versions have tuxcare suffix."""
        # If repo actually has TuxCare version, it should match
        self.assertTrue(
            VersionMatcher.versions_match("1.2.17.tuxcare.1", "1.2.17.tuxcare.1")
        )
        
        # Different TuxCare versions should match base version
        self.assertTrue(
            VersionMatcher.versions_match("1.2.17.tuxcare.1", "1.2.17.tuxcare.2")
        )
    
    def test_versions_match_complex_versions(self):
        """Test with complex version strings."""
        # Guava example: 30.1-jre with TuxCare suffix
        self.assertTrue(
            VersionMatcher.versions_match("30.1-jre.tuxcare", "30.1-jre.tuxcare")
        )
        
        # Vanilla version should not match
        self.assertFalse(
            VersionMatcher.versions_match("30.1-jre", "30.1-jre.tuxcare")
        )
        
        # Different qualifier should not match
        self.assertFalse(
            VersionMatcher.versions_match("30.1-android.tuxcare", "30.1-jre.tuxcare")
        )
    
    def test_versions_match_empty(self):
        """Test with empty version strings."""
        self.assertFalse(
            VersionMatcher.versions_match("", "1.2.17.tuxcare.1")
        )
        
        self.assertFalse(
            VersionMatcher.versions_match("1.2.17", "")
        )
        
        self.assertFalse(
            VersionMatcher.versions_match("", "")
        )
    
    def test_versions_match_log4j_scenario(self):
        """Test the specific log4j scenario from the issue."""
        # Scenario: User has log4j:log4j:1.2.17 in pom.xml (vanilla version)
        #           VEX has log4j:log4j:1.2.17.tuxcare.1 as patched
        #           Expected: NO MATCH (alert should NOT be dismissed)
        # 
        # Reason: User doesn't have the TuxCare patched version, so they don't have the fix
        self.assertFalse(
            VersionMatcher.versions_match("1.2.17", "1.2.17.tuxcare.1")
        )
        
        # Scenario: User upgrades to use TuxCare patched version in pom.xml
        #           VEX has log4j:log4j:1.2.17.tuxcare.1 as patched
        #           Expected: MATCH (alert should be dismissed)
        #
        # Reason: User is now using the TuxCare patched version with the fix
        self.assertTrue(
            VersionMatcher.versions_match("1.2.17.tuxcare.1", "1.2.17.tuxcare.1")
        )


if __name__ == "__main__":
    unittest.main()

