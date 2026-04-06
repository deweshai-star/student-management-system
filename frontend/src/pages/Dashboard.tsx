import { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../api/client';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { Input } from '../components/ui/input';
import { LogOut, GraduationCap, Search, User as UserIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Student {
  id: number;
  name: string;
  student_id: string;
  grade: string;
  enrollment_date: string;
}

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [students, setStudents] = useState<Student[]>([]);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.role === 'admin' || user?.role === 'teacher') {
      fetchStudents(search);
    } else if (user?.role === 'student') {
      fetchMyProfile();
    }
  }, [user, search]);

  const fetchStudents = async (searchQuery: string) => {
    try {
      const response = await apiClient.get(`/students/?search=${searchQuery}`);
      setStudents(response.data);
    } catch (error) {
      console.error('Failed to fetch students', error);
    }
  };

  const fetchMyProfile = async () => {
    try {
      const response = await apiClient.get('/students/me');
      setStudents([response.data]);
    } catch (error) {
      console.error('Failed to fetch profile', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen flex bg-slate-50 dark:bg-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 p-6 flex flex-col">
        <div className="flex items-center gap-2 mb-10 text-primary">
          <GraduationCap size={32} />
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">EduManage</h1>
        </div>
        
        <nav className="flex-1 space-y-2">
          <Button variant="secondary" className="w-full justify-start gap-2">
            <UserIcon size={18} /> Dashboard
          </Button>
          {/* Add more nav items based on role if needed */}
        </nav>
        
        <div className="mt-auto">
          <div className="mb-4 text-sm text-slate-500 text-center capitalize w-full">Role: {user?.role}</div>
          <Button variant="outline" className="w-full gap-2 text-destructive" onClick={handleLogout}>
            <LogOut size={18} /> Logout
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-auto">
        <div className="mb-8">
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Welcome back, {user?.email}</h2>
          <p className="text-muted-foreground mt-1 text-lg">Here's an overview of the system.</p>
        </div>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
            <CardTitle>{user?.role === 'student' ? 'My Profile' : 'Student Registry'}</CardTitle>
            {(user?.role === 'admin' || user?.role === 'teacher') && (
              <div className="relative w-64">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="search"
                  placeholder="Search students..."
                  className="pl-8"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
            )}
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Student ID</TableHead>
                  <TableHead>Grade</TableHead>
                  <TableHead>Enrollment</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {students.map((student) => (
                  <TableRow key={student.id}>
                    <TableCell className="font-medium">{student.id}</TableCell>
                    <TableCell>{student.name}</TableCell>
                    <TableCell>{student.student_id}</TableCell>
                    <TableCell>{student.grade}</TableCell>
                    <TableCell>{student.enrollment_date}</TableCell>
                  </TableRow>
                ))}
                {students.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center h-24 text-muted-foreground">
                      No students found.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
