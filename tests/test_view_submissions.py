from pyramid import testing

from base import (
    UnitTestBase,
    IntegrationTestBase,
)


class UnitTest(UnitTestBase):
    def test_post_submission_succeeds(self):
        """Make sure we can post a new submission"""
        from cloudbenchmarksorg.views.submissions import submissions_post

        request = testing.DummyRequest(
            json_body=self.submission_data
        )

        response = submissions_post(request)
        self.assertEqual(response, {})

    def test_post_submission_fails(self):
        """Make sure we can't post garbage data as a new submission"""
        from cloudbenchmarksorg.views.submissions import submissions_post

        request = testing.DummyRequest(
            json_body={}
        )

        response = submissions_post(request)
        self.assertTrue('errors' in response)

    def test_get_submissions_succeeds(self):
        """Make sure we can get list of new submissions"""
        from cloudbenchmarksorg.views.submissions import submissions_get

        self.load_test_submission()

        request = testing.DummyRequest()
        response = submissions_get(request)
        self.assertEqual(
            response['submissions_query'].count(),
            1
        )

    def test_show_submission_succeeds(self):
        """Make sure we can get list of new submissions"""
        from cloudbenchmarksorg.views.submissions import submission_show

        submission = self.load_test_submission()

        request = testing.DummyRequest()
        request.matchdict['id'] = submission.id
        response = submission_show(request)
        self.assertEqual(
            response['submission'].id,
            submission.id
        )


class IntegrationTest(IntegrationTestBase):
    def test_post_submission_succeeds(self):
        """ POST new submission

        POST /submissions 200

        """
        from cloudbenchmarksorg import models as M
        self.app.post_json('/submissions', self.submission_data)

        self.assertEqual(
            self.session.query(M.Submission).count(), 1)

    def test_post_submission_fails(self):
        """ POST invalid submission

        POST /submissions 400

        """
        from cloudbenchmarksorg import models as M
        res = self.app.post_json('/submissions', {}, status=400)

        self.assertTrue('errors' in res.json)
        self.assertEqual(
            self.session.query(M.Submission).count(), 0)

    def test_get_submissions(self):
        """ GET Submissions list

        GET /submissions 200

        """
        # load a test submission first
        self.app.post_json('/submissions', self.submission_data)
        self.app.get('/submissions')

    def test_show_submission(self):
        """ GET Submission

        GET /submission/:id 200

        """
        # load a test submission first
        submission = self.load_test_submission()
        self.app.get('/submissions/{}'.format(submission.id))
        self.app.get('/submissions/{}'.format(submission.id + 1), status=404)
