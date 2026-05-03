import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Advisor from '../pages/Advisor';

// Mock fetch
global.fetch = jest.fn();

describe('Advisor Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const renderAdvisor = () => {
    return render(
      <MemoryRouter>
        <Advisor />
      </MemoryRouter>
    );
  };

  test('renders advisor page with form', () => {
    renderAdvisor();
    
    expect(screen.getByText('Scheme Advisor')).toBeInTheDocument();
    expect(screen.getByText('Tell us about yourself')).toBeInTheDocument();
    expect(screen.getByLabelText('Age *')).toBeInTheDocument();
    expect(screen.getByLabelText('Annual Income (₹) *')).toBeInTheDocument();
    expect(screen.getByLabelText('Occupation')).toBeInTheDocument();
    expect(screen.getByLabelText('Education')).toBeInTheDocument();
    expect(screen.getByLabelText('State')).toBeInTheDocument();
    expect(screen.getByLabelText('Category')).toBeInTheDocument();
  });

  test('form validation works', async () => {
    renderAdvisor();
    
    // Try to search without filling required fields
    const searchButton = screen.getByText('🔍 Search Schemes');
    fireEvent.click(searchButton);
    
    // Should show alert for missing required fields
    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('Please fill in at least age and income for personalized recommendations');
    });
  });

  test('search functionality works', async () => {
    // Mock successful API response
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        data: [
          {
            id: 'scheme_001',
            name: 'National Scholarship Portal',
            category: 'education',
            description: 'Centralized platform for various scholarship schemes',
            benefits: 'Financial assistance for education',
            documents_required: ['Aadhaar card', 'Mark sheets'],
            eligibility_criteria: ['Students from class 1 to post-graduation'],
            state: 'All India',
            income_limit: 250000,
            official_link: 'https://scholarships.gov.in',
            similarity_score: 0.92,
            confidence_score: 0.88,
            why_eligible: 'Based on your student profile',
            application_steps: ['Register on scholarships.gov.in']
          }
        ],
        total_results: 1,
        search_time: 0.001,
        search_method: 'rag_llm'
      })
    });

    renderAdvisor();
    
    // Fill form
    fireEvent.change(screen.getByLabelText('Age *'), { target: { value: '21' } });
    fireEvent.change(screen.getByLabelText('Annual Income (₹) *'), { target: { value: '250000' } });
    fireEvent.change(screen.getByLabelText('Occupation'), { target: { value: 'student' } });
    fireEvent.change(screen.getByLabelText('Education'), { target: { value: 'engineering' } });
    fireEvent.change(screen.getByLabelText('State'), { target: { value: 'Karnataka' } });
    fireEvent.change(screen.getByLabelText('Category'), { target: { value: 'education' } });
    
    // Click search button
    const searchButton = screen.getByText('🔍 Search Schemes');
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/schemes/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: expect.stringContaining('scholarship for students')
      });
    });
  });

  test('recommend functionality works', async () => {
    // Mock successful API response
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        recommendations: [
          {
            id: 'scheme_001',
            name: 'National Scholarship Portal',
            category: 'education',
            description: 'Centralized platform for various scholarship schemes',
            benefits: 'Financial assistance for education',
            documents_required: ['Aadhaar card', 'Mark sheets'],
            eligibility_criteria: ['Students from class 1 to post-graduation'],
            state: 'All India',
            income_limit: 250000,
            official_link: 'https://scholarships.gov.in',
            eligibility_score: 0.92,
            benefit_score: 0.85,
            overall_score: 0.88,
            personalized_reasoning: 'Based on your profile',
            application_priority: 'high',
            next_steps: ['Gather documents'],
            recommendation_strength: 'strong'
          }
        ],
        total_recommendations: 1,
        response_time: 0.002,
        recommendation_method: 'personalized'
      })
    });

    renderAdvisor();
    
    // Fill form
    fireEvent.change(screen.getByLabelText('Age *'), { target: { value: '25' } });
    fireEvent.change(screen.getByLabelText('Annual Income (₹) *'), { target: { value: '400000' } });
    fireEvent.change(screen.getByLabelText('Occupation'), { target: { value: 'private employee' } });
    fireEvent.change(screen.getByLabelText('Education'), { target: { value: 'graduate' } });
    fireEvent.change(screen.getByLabelText('State'), { target: { value: 'Delhi' } });
    
    // Click recommend button
    const recommendButton = screen.getByText('🤖 Get Recommendations');
    fireEvent.click(recommendButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/schemes/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: expect.stringContaining('personalized recommendations')
      });
    });
  });

  test('displays search results correctly', async () => {
    // Mock successful API response
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        data: [
          {
            id: 'scheme_001',
            name: 'National Scholarship Portal',
            category: 'education',
            description: 'Centralized platform for various scholarship schemes',
            benefits: 'Financial assistance for education covering tuition fees',
            documents_required: ['Aadhaar card', 'Mark sheets', 'Income certificate'],
            eligibility_criteria: ['Students from class 1 to post-graduation'],
            state: 'All India',
            income_limit: 250000,
            official_link: 'https://scholarships.gov.in',
            similarity_score: 0.92,
            confidence_score: 0.88,
            why_eligible: 'Based on your student profile and income level',
            application_steps: ['Register on scholarships.gov.in', 'Complete profile']
          }
        ],
        total_results: 1,
        search_time: 0.001,
        search_method: 'rag_llm'
      })
    });

    renderAdvisor();
    
    // Fill form and search
    fireEvent.change(screen.getByLabelText('Age *'), { target: { value: '21' } });
    fireEvent.change(screen.getByLabelText('Annual Income (₹) *'), { target: { value: '250000' } });
    
    const searchButton = screen.getByText('🔍 Search Schemes');
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText('Search Results')).toBeInTheDocument();
      expect(screen.getByText('National Scholarship Portal')).toBeInTheDocument();
      expect(screen.getByText('88% Match')).toBeInTheDocument();
      expect(screen.getByText('92% Similar')).toBeInTheDocument();
      expect(screen.getByText('💡 Why you\'re eligible:')).toBeInTheDocument();
      expect(screen.getByText('💰 Benefits:')).toBeInTheDocument();
      expect(screen.getByText('📋 Required Documents:')).toBeInTheDocument();
      expect(screen.getByText('📝 How to Apply:')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    // Mock API error
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    renderAdvisor();
    
    // Fill form and search
    fireEvent.change(screen.getByLabelText('Age *'), { target: { value: '21' } });
    fireEvent.change(screen.getByLabelText('Annual Income (₹) *'), { target: { value: '250000' } });
    
    const searchButton = screen.getByText('🔍 Search Schemes');
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(window.alert).toHaveBeenCalledWith('Failed to search schemes. Please try again.');
    });
  });

  test('displays loading state', async () => {
    // Mock slow API response
    (fetch as jest.Mock).mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({
          success: true,
          data: [],
          total_results: 0,
          search_time: 0.001,
          search_method: 'rag_llm'
        })
      }), 100))
    );

    renderAdvisor();
    
    // Fill form and search
    fireEvent.change(screen.getByLabelText('Age *'), { target: { value: '21' } });
    fireEvent.change(screen.getByLabelText('Annual Income (₇) *'), { target: { value: '250000' } });
    
    const searchButton = screen.getByText('🔍 Search Schemes');
    fireEvent.click(searchButton);
    
    // Should show loading state
    expect(screen.getByText('Searching...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('No schemes found')).toBeInTheDocument();
    }, { timeout: 200 });
  });

  test('displays empty state when no results', async () => {
    // Mock empty API response
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        data: [],
        total_results: 0,
        search_time: 0.001,
        search_method: 'rag_llm'
      })
    });

    renderAdvisor();
    
    // Fill form and search
    fireEvent.change(screen.getByLabelText('Age *'), { target: { value: '21' } });
    fireEvent.change(screen.getByLabelText('Annual Income (₇) *'), { target: { value: '250000' } });
    
    const searchButton = screen.getByText('🔍 Search Schemes');
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText('No schemes found')).toBeInTheDocument();
      expect(screen.getByText('Try adjusting your search criteria or filters')).toBeInTheDocument();
    });
  });
});

describe('Advisor Component Form', () => {
  test('state dropdown has all Indian states', () => {
    render(
      <MemoryRouter>
        <Advisor />
      </MemoryRouter>
    );
    
    const stateSelect = screen.getByLabelText('State');
    expect(stateSelect).toBeInTheDocument();
    
    // Check for some key states
    expect(screen.getByText('Select your state')).toBeInTheDocument();
    expect(screen.getByText('All India')).toBeInTheDocument();
    expect(screen.getByText('Maharashtra')).toBeInTheDocument();
    expect(screen.getByText('Karnataka')).toBeInTheDocument();
    expect(screen.getByText('Delhi')).toBeInTheDocument();
  });

  test('category dropdown has all categories', () => {
    render(
      <MemoryRouter>
        <Advisor />
      </MemoryRouter>
    );
    
    const categorySelect = screen.getByLabelText('Category');
    expect(categorySelect).toBeInTheDocument();
    
    // Check for key categories
    expect(screen.getByText('All Categories')).toBeInTheDocument();
    expect(screen.getByText('education')).toBeInTheDocument();
    expect(screen.getByText('agriculture')).toBeInTheDocument();
    expect(screen.getByText('healthcare')).toBeInTheDocument();
    expect(screen.getByText('housing')).toBeInTheDocument();
  });

  test('form inputs accept correct data types', () => {
    render(
      <MemoryRouter>
        <Advisor />
      </MemoryRouter>
    );
    
    // Test age input (number)
    const ageInput = screen.getByLabelText('Age *');
    expect(ageInput).toHaveAttribute('type', 'number');
    expect(ageInput).toHaveAttribute('min', '1');
    expect(ageInput).toHaveAttribute('max', '100');
    
    // Test income input (number)
    const incomeInput = screen.getByLabelText('Annual Income (₇) *');
    expect(incomeInput).toHaveAttribute('type', 'number');
    expect(incomeInput).toHaveAttribute('min', '0');
    expect(incomeInput).toHaveAttribute('step', '10000');
  });
});
