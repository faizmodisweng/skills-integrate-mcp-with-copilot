# Draft issues to add - SLIIT RSVP feature set

Below are proposed GitHub issues to implement the features we discussed. Review and tell me which to create as real issues on GitHub. Each issue includes a title, description, acceptance criteria, and suggested labels/estimate.

---

1) Title: Scaffold React SPA and routing

Description:
Set up a minimal React single-page application inside the repository to replace the current static frontend. The SPA should use Create React App (or Vite if preferred) and include routing via `react-router` with a basic Navbar and Footer components.

Acceptance criteria:
- New `frontend/` directory created with a React app scaffold (or instructions to install dependencies).
- App mounts at `/` and is served by the existing FastAPI static mount (or updated instructions provided).
- Routes: `/` (Home), `/events`, `/clubs`, `/contact` are configured and render placeholder components.
- Basic Navbar and Footer components implemented and visible on all routes.

Labels: enhancement, frontend, setup
Estimate: 3-5 points

---

2) Title: Implement Events page and `EventCard` component

Description:
Add an `Events` route and implement a reusable `EventCard` React component that displays event image, title, community name, date range, attendee count, and RSVP button. Integrate it with the existing `GET /activities` API so event data is loaded from the backend.

Acceptance criteria:
- `EventCard` component created with props for `title`, `community`, `image`, `fromDate`, `toDate`, `attendees`.
- `Events` page fetches data from `/activities` and maps activities to `EventCard` instances.
- RSVP button opens a small modal or triggers signup using the existing `POST /activities/{name}/signup?email=` endpoint.
- Component styling included (SCSS or CSS module) mimicking card layout.

Labels: enhancement, frontend, api-integration
Estimate: 5-8 points

---

3) Title: Add Ticket component for printable tickets

Description:
Create a stylized `Ticket` React component to present RSVP'd attendees with a printable ticket layout (avatar, attendee name, event, date, venue, ticket id). Provide a Print button to print the ticket view.

Acceptance criteria:
- `Ticket` component implemented and styled.
- Tickets render a unique ticket id (client-generated is acceptable) and attendee info.
- A Print button triggers the browser print dialog with a clean ticket-only print stylesheet.

Labels: feature, frontend, ux
Estimate: 3-5 points

---

4) Title: Clubs directory page

Description:
Implement `Clubs` route that shows a responsive grid of club tiles (image + short description + More Info action). Support a detail modal or separate club page when 'More Info' is clicked.

Acceptance criteria:
- `Clubs` page lists clubs pulled from the backend (or a client-side seed list if backend extension is needed).
- 'More Info' shows additional club details via modal or detail route.

Labels: enhancement, frontend
Estimate: 3 points

---

5) Title: Add React Query and replace manual fetches

Description:
Introduce `react-query` (TanStack Query) to manage data fetching, caching, and background updates. Replace existing direct fetch logic in the React app with query hooks.

Acceptance criteria:
- `react-query` added to dependencies and `QueryClientProvider` set up at app root.
- Activities fetching uses `useQuery` and signup/unregister use `useMutation` patterns.
- UI shows loading and error states consistent across pages.

Labels: improvement, frontend, tech-debt
Estimate: 2-4 points

---

6) Title: Add Login UI (Google button + email form)

Description:
Add a Login page with a Google sign-in button UI and an email/password sign-in form. This will be UI-only initially; later we can integrate OAuth or an auth backend.

Acceptance criteria:
- Login page route `/login` with Google button and email form.
- Form validations (email format) and UI feedback for invalid inputs.
- Placeholder callback handlers or TODO comments for OAuth integration.

Labels: feature, frontend, auth
Estimate: 2-3 points

---

7) Title: Contact page and contact form submission

Description:
Implement a Contact page within the SPA that contains a contact form (Name, Email, Subject, Message). Hook it to a simple API endpoint or store messages locally for now.

Acceptance criteria:
- `/contact` route shows contact form.
- Form validates inputs and shows success/error messages after submit.
- (Optional) Add `POST /contact` API endpoint to the FastAPI app to receive messages.

Labels: enhancement, frontend, api-integration
Estimate: 2-4 points

---

8) Title: Move static frontend assets into `frontend/` and update FastAPI static mount

Description:
When converting to a React SPA, move existing `src/static` files into a `frontend/` project or adjust the static mounting so production build files are served from the proper directory.

Acceptance criteria:
- Clear directory layout and README update describing how to run frontend and backend for development and production.
- FastAPI static mount updated or documented to serve built files.

Labels: maintenance, infra
Estimate: 1-2 points

---

9) Title: Persist activities to a simple database (SQLite)

Description:
Replace in-memory `activities` store with a persistent storage layer (SQLite via SQLModel or SQLAlchemy). Add simple migrations or initialization code and update API handlers to use the DB.

Acceptance criteria:
- Activities persisted in SQLite; server restarts keep data.
- Signup/unregister endpoints update the DB accordingly.
- Provide seed script or initial DB migration.

Labels: backend, database, enhancement
Estimate: 5-8 points

---

10) Title: Protect signup/unregister endpoints with basic auth or token

Description:
Add simple authentication or token protection for endpoints that modify activity signups to prevent abuse (initially basic token or API key stored in env).

Acceptance criteria:
- Protected endpoints require a header or token; unauthorized requests return 401.
- README updated with usage instructions.

Labels: security, backend
Estimate: 2-4 points

---

If this list looks good, tell me which issues to create on GitHub. I can either:
- Create all issues in your repository automatically (I will need permission / token), or
- Create just a subset you select, or
- Commit this file and wait for your confirmation before creating real GitHub issues.
