"""Git state collection tests — clean repo, dirty repo, branch detection."""

import unittest

from traceweave.git_state import GitError, collect

from helpers import new_repo, run_git


class TestGitState(unittest.TestCase):

    def test_clean_repository(self):
        repo = new_repo()
        state = collect(repo)
        self.assertEqual(state.working_tree, "clean")
        self.assertEqual(state.changed_files, [])
        self.assertIsNotNone(state.head_commit)
        self.assertEqual(len(state.head_commit), 40)

    def test_dirty_repository(self):
        repo = new_repo()
        (repo / "new-file.txt").write_text("untracked\n", encoding="utf-8")
        state = collect(repo)
        self.assertEqual(state.working_tree, "dirty")
        self.assertIn("new-file.txt", state.changed_files)

    def test_branch_detection(self):
        repo = new_repo()
        run_git(repo, "checkout", "-q", "-b", "feature/traceweave-test")
        state = collect(repo)
        self.assertEqual(state.branch, "feature/traceweave-test")

    def test_remote_credentials_are_not_persisted(self):
        repo = new_repo()
        run_git(repo, "remote", "add", "origin", "https://user:super-secret@example.com/owner/repo.git?token=abc#frag")
        state = collect(repo)
        self.assertEqual(state.repository, "example.com/owner/repo.git")
        self.assertNotIn("super-secret", state.repository)
        self.assertNotIn("token=", state.repository)
        self.assertNotIn("user@", state.repository)

    def test_local_remote_falls_back_to_repo_name(self):
        repo = new_repo()
        run_git(repo, "remote", "add", "origin", "/private/machine/path/repo.git")
        state = collect(repo)
        self.assertEqual(state.repository, repo.name)

    def test_untracked_filename_with_spaces_is_preserved(self):
        repo = new_repo()
        (repo / "file with spaces.txt").write_text("x\n", encoding="utf-8")
        state = collect(repo)
        self.assertIn("file with spaces.txt", state.changed_files)

    def test_rename_records_destination_path(self):
        repo = new_repo()
        run_git(repo, "mv", "README.md", "README renamed.md")
        state = collect(repo)
        self.assertIn("README renamed.md", state.changed_files)
        self.assertNotIn("README.md", state.changed_files)

    def test_outside_repository_raises(self):
        import tempfile
        with tempfile.TemporaryDirectory(prefix="traceweave-nogit-") as tmp:
            with self.assertRaises(GitError):
                collect(__import__("pathlib").Path(tmp))


if __name__ == "__main__":
    unittest.main()
