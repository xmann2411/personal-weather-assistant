import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { PlanResponse } from './types/plan';

const plan: PlanResponse = {
  location: { name: 'Zagreb', country: 'HR', lat: 45.81, lon: 15.98 },
  date: '2026-10-21',
  weather: { min: 9, max: 14, feels: 12, wind: 9.5, pop: 70, uv: null, humidity: 80, desc: 'umjerena kiša', icon: '10d' },
  plan: {
    outfit: { top: 'džemper', bottom: 'traperice', outerwear: 'vodootporna jakna', shoes: 'čizme', accessories: ['kišobran'] },
    activities: [{ name: 'Muzej Mimara', indoor: true, timeSuggestion: 'morning', note: 'zaklon od kiše' }],
    alerts: [{ type: 'rain', message: 'Ponesi kišobran.' }],
    packing: ['rezervne čarape'],
    rationale: 'Kišovit dan.',
  },
  source: 'fallback',
};

function mockFetch(status: number, body: unknown) {
  global.fetch = jest.fn().mockResolvedValue({
    ok: status < 400,
    status,
    text: () => Promise.resolve(JSON.stringify(body)),
  }) as jest.Mock;
}

async function submitCity(city: string) {
  await userEvent.type(screen.getByLabelText('Grad'), city);
  await userEvent.click(screen.getByRole('button', { name: /generiraj plan/i }));
}

beforeEach(() => localStorage.clear());

test('renders title and search form', () => {
  render(<App />);
  expect(screen.getByRole('heading', { name: /vakula 2.0/i })).toBeInTheDocument();
  expect(screen.getByLabelText('Grad')).toBeInTheDocument();
});

test('shows the plan returned by the backend', async () => {
  mockFetch(200, plan);
  render(<App />);
  await submitCity('Zagreb');

  expect(await screen.findByText('Muzej Mimara')).toBeInTheDocument();
  expect(screen.getByText(/ujutro/)).toBeInTheDocument();
  expect(screen.getByText(/Kiša/, { selector: 'strong' })).toBeInTheDocument();
  expect(screen.getByText(/AI servis trenutno nije dostupan/)).toBeInTheDocument();

  const [, options] = (global.fetch as jest.Mock).mock.calls[0];
  expect(JSON.parse(options.body)).toMatchObject({ city: 'Zagreb' });
});

test('shows backend error message', async () => {
  mockFetch(404, { detail: 'Grad „Xyz” nije pronađen.' });
  render(<App />);
  await submitCity('Xyz');

  expect(await screen.findByRole('alert')).toHaveTextContent('Grad „Xyz” nije pronađen.');
});
