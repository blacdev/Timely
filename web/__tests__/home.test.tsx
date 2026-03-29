import { render, screen } from '@testing-library/react';
import Home from '../pages/index';

describe('Home', () => {
  it('renders overview cards', () => {
    render(<Home />);
    expect(screen.getByText('Overview')).toBeInTheDocument();
  });
});
