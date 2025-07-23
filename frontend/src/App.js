import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [subjects, setSubjects] = useState([]);
  const [attendance, setAttendance] = useState({});

  useEffect(() => {
    fetchSubjects();
  }, []);

  const fetchSubjects = async () => {
    try {
      const response = await axios.get('http://localhost:5000/subjects');
      setSubjects(response.data);
      // Initialize attendance state
      const initialAttendance = {};
      response.data.forEach(subject => {
        initialAttendance[subject.id] = false;
      });
      setAttendance(initialAttendance);
    } catch (error) {
      console.error('Error fetching subjects:', error);
    }
  };

  const handleAttendanceChange = (subjectId) => {
    setAttendance(prev => ({
      ...prev,
      [subjectId]: !prev[subjectId]
    }));
  };

  const submitAttendance = async () => {
    const today = new Date().toISOString().split('T')[0];
    try {
      for (const subjectId in attendance) {
        await axios.post('http://localhost:5000/attendance', {
          subject_id: parseInt(subjectId),
          date: today,
          attended: attendance[subjectId]
        });
      }
      alert('Attendance submitted successfully!');
    } catch (error) {
      console.error('Error submitting attendance:', error);
      alert('Failed to submit attendance.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Academic Planner - Attendance</h1>
      <table border="1" cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>Course Code</th>
            <th>Course Title</th>
            <th>Attended Today</th>
          </tr>
        </thead>
        <tbody>
          {subjects.map(subject => (
            <tr key={subject.id}>
              <td>{subject.course_code}</td>
              <td>{subject.course_title}</td>
              <td>
                <input
                  type="checkbox"
                  checked={attendance[subject.id] || false}
                  onChange={() => handleAttendanceChange(subject.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={submitAttendance} style={{ marginTop: '20px' }}>
        Submit Attendance
      </button>
    </div>
  );
}

export default App;
